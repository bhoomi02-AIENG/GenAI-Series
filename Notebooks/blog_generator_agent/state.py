from pydantic import BaseModel
class BlogState(BaseModel):
    
    # USER INPUT
    topic : str = ""
    audience : str = "general reader"
    
    
    # RESEARCHER OUTPUT
    research : str = ""
    research_feedback : str = ""

    
    # WRITER OUTPUT
    draft : str = ""
    draft_feedback : str = ""

    
    # EDITOR OUTPUT
    final_blog : str = ""

    
    # METADATA 
    revision_count: int = 0