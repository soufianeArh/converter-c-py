#evaluate chunks
###get context (chunks) of the tests.question []
###compare the chunks with keywords

from .test_loader import load_tests, TestDictValidator
from implementations.question import retrieveChunks
from pydantic import BaseModel

class RetrialEval(BaseModel):
      mrr: float

def calculateMRR (chunks:list, keyword:str) -> float:
      keyword_lower = keyword.lower()
      for rank, chunk in enumerate(chunks, start=1):
            if keyword_lower in chunk.page_content.lower():
                  return 1.0/rank
      return 0.0
def evalSingleChunk(test: TestDictValidator):
      # get the chunks
      chunks = retrieveChunks(test.question)
      # calculare mrr: finality is have an arra of scores each score repressnt position of kw in chunks
      mrr_values= [calculateMRR(chunks,keyworld) for keyworld in test.keywords]
      mrr_avg= sum(mrr_values)/len(mrr_values) if mrr_values else 0.0
      # calculate 
      # Calculate keyword coverage

      # mrr=avg_mrr,ndcg=avg_ndcg,keywords_found=keywords_found, total_keywords=total_keywords,keyword_coverage=keyword_coverage,
      return RetrialEval(
            mrr=mrr_avg
      )
def evalAllChunks():
      ""
      #get all the tests
      tests= load_tests()
      evalSingleChunk(tests[0])
      #loop eval Single Chunk and get the eval object
      #

if __name__ == "__main__":
      evalAllChunks()