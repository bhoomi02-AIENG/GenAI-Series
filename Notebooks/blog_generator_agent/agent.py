import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# GET LLM
def get_llm(model_name: str = "openai/gpt-oss-20b", temperature: float = 0.5):
    api_key=os.getenv("GROQ_API_KEY")
    llm=ChatGroq(model=model_name, temperature=temperature, api_key=api_key)
    return llm

# RESEARCH AGENT
RESEARCHER_PROMPT=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
        "You are a Reasearch Agent. Given a blog topic and target audience, produce a clear, "
        "structured research outline. Include:\n"
        "1. 5-7 key points the blog should cover\n"
        "2. Important facts, stats, or examples for each point\n"
        "3. Suggested angle or hook\n"
        "Be concise. Use bullet points. DO Not write the full blog yet."
      
    """},
    {"role":"user","content":"Topic: {topic}, Audience:{audience},{revision_hints}, write the research outline now."}
])

def researcher_agent(llm:ChatGroq, topic: str, audience: str, feedback: str = ""):
    revision_hints=f"The human provided this feedback on your previous research - please address it: {feedback}."
    if not feedback:
        revision_hints="This is your first attempt."
    chain = RESEARCHER_PROMPT | llm
    result=chain.invoke({
        "topic":topic,
        "audience":audience,
        "revision_hints":revision_hints
    })
    return result.content

# WRITER AGENT
WRITER_PROMPT=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
        "You are a Blog Writer Agent. Using the research notes provided, write a complete,"
        "engaging blog post.\n"
        "Rules:\n"
        "- Length: 500-800 words\n"
        "- Structure: catchy title, intro hook.3-5 sections with H2 headings, conclusion\n"
        "- Tone: clear, friendly, suited to the target audience\n"
        "- Use markdown formatting\n"
        "- Do Not add a 'word count' Line at the end"
        
      
    """},
    {"role":"user","content":"""
            topic: {topic},
            Audience: {audience},
            Research Notes: {research}
            
            {revision_hints}
            write the full blog post now.
          
    """}
])

def writer_agent(llm:ChatGroq, topic: str, audience: str, research: str = "", feedback: str = "") -> str:
    revision_hints=f"The human provided this feedback on your previous draft and asked for thses changes:{feedback}. Please apply these changes during writing the blog."
    if not feedback:
        revision_hints="This is your first attempt."
    
    chain = WRITER_PROMPT | llm
    result=chain.invoke({
        "topic":topic,
        "audience":audience,
        "research":research,
        "revision_hints":revision_hints
    })
    return result.content

# EDITOR AGENT
EDITOR_PROMPT=ChatPromptTemplate.from_messages([
    {"role":"system","content":"""
        "You are a Editor Agent - the final quality gate before publishing.\n"
        "Take the darft and produce the FINAL polished version. Specifically:\n"
        "- Fix grammer, spelling and awkard phrasing\n"
        "- Tighten wordy sentences\n"
        "- Improve flow and transitions between sections\n"
        "- Make the title and intro more compelling if needed\n"
        "- Keep the same structure and markdown formatting\n"
        "- Blog wordings should like human, not lik a AI, and don't use any special chars and complex/fancy words.\n"
        "- Output only the final polished blog post - no commentary."
        
      
    """},
    {"role":"user","content":"""
            topic: {topic},
            Draft: {draft}
            
            Return the published blog post.
          
    """}
])


def editor_agent(llm:ChatGroq, topic: str, draft: str = "") -> str:

    
    chain = EDITOR_PROMPT | llm
    result=chain.invoke({
        "topic":topic,
        "draft":draft,
        
    })
    return result.content

