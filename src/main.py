from navs.labcorp import LabCorpSearch
from navs.quest import QuestSearch

lc_search = LabCorpSearch(
    57007, 
    radius=100, 
    service=LabCorpSearch.DRUG_SCREEN_COLLECTION
)

q_search = QuestSearch(
    92108,
)

q_search.search()