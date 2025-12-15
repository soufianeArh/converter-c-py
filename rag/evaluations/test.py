#load the tests via open iterator
#switch them to py DIct
#appens to tests list (with check)

import json
from pathlib import Path
from pydantic import BaseModel
FILE_PATH=str(Path(__file__).parent / "tests.jsonl")

class TestDictValidator(BaseModel):
      question: str
      keywords: list
      reference_answer: str
      category: str

def load_tests():
      tests=[]
      with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                  data= json.loads(next(f).strip())
                  tests.append(TestDictValidator(**data))
      return tests

if __name__ == "__main__":
      print(load_tests())
