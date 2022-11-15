

# pydov.hooks.append(
#     RepeatableLogRecorder('.')
# )


from pydov.util.hooks import RepeatableLogReplayer
from pydov.search.boring import BoringSearch
import pydov
import sys
sys.path.insert(0, './pydov-archive-20221006T152243-498f7b.zip')


pydov.hooks.append(
    RepeatableLogReplayer('./pydov-archive-20221006T152243-498f7b.zip')
)
s = BoringSearch()
df = s.search(max_features=20)
print(df)
