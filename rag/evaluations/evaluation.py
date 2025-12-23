#evaluate chunks
###get context (chunks) of the tests.question []
###compare the chunks with keywords

from .test_loader import load_tests, TestDictValidator
from implementations.question import retrieveChunks
from pydantic import BaseModel
import math

class RetrialEval(BaseModel):
      mrr: float
      ndgc: float
      keywords_found: float
      total_keywords: float
      keyword_coverage = float

def calculateDCG (relavance):
      dcg=0.0
      for i in range(len(relavance)):
            dcg+=relavance[i] / math.log2(i+2)
      return dcg

def calculateMRR (chunks:list, keyword:str) -> float:
      keyword_lower = keyword.lower()
      for rank, chunk in enumerate(chunks, start=1):
            if keyword_lower in chunk.page_content.lower():
                  return 1.0/rank
      return 0.0

def calcilateNDCG ( chunks:list,keyword: str, k: int=10):
      keyword_lower = keyword.lower()
      # relecance list of kw ex: [0,1,1,0,0] kw match in 2,3 chucks
      relevances = [
            1 if keyword_lower in  chunk.page_content.lower() else 0 for chunk in chunks[:k]
      ]
      dcg = calculateDCG(relevances)
      ideal_relevances = sorted(relevances, reverse=True)
      idgc = calculateDCG(ideal_relevances)

      return dcg / idgc if idgc > 0 else 0
      
def evalSingleTest(test: TestDictValidator) -> RetrialEval:
      # get the chunks
      chunks = retrieveChunks(test.question)
      # calculare mrr: finality is have an arra of scores each score repressnt position of kw in chunks
      # avg_mrr = 0.5 means ?
      mrr_values= [calculateMRR(chunks,keyworld) for keyworld in test.keywords]
      mrr_avg= sum(mrr_values)/len(mrr_values) if mrr_values else 0.0
      # calculate ndcg: 
      ndgc_values = [calcilateNDCG(chunks,keyword) for keyword in test.keywords]
      ndcg_avg = sum(ndgc_values) / len(ndgc_values) if ndgc_values else 0
      # Calculate keyword coverage
      ## mrr_values [0,1,0.2] = 1.2
      keywords_found=sum(1 for score in mrr_values if score > 0)
      total_keywords = len(test.keywords)
      keyword_coverage = (keywords_found / total_keywords * 100) if total_keywords > 0 else 0.0

      return RetrialEval(
            mrr=mrr_avg,
            ndgc=ndcg_avg,
            keywords_found=keywords_found,
            total_keywords=total_keywords,
            keyword_coverage=keyword_coverage
      )

def evalAllTests():
      ""
      #get all the tests
      tests= load_tests()
      print(evalSingleTest(tests[1]))
      #loop eval Single Chunk and get the eval object
      #

if __name__ == "__main__":
      evalAllTests()