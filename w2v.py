import gensim
import pandas as pd
import streamlit as st
import numpy as np
import SessionState
from accords_list import accords_x1, accord_list
model2 = gensim.models.Word2Vec.load('word2vec.model')

st.sidebar.image("border_color_black_24dp.svg", use_column_width=None)

scent = st.sidebar.selectbox("노트를 골라 주세요. (키 입력 지원)",accord_list)

# scent = st.text_input('Input Perfume note:')
st.image("GSC_campaign-life-energy-iN-perfume-180421-1.jpg", use_column_width=True)
st.title("향수 추천 Word2Vec")
st.write(f'선택한 노트는{scent} 입니다.')
#=========================================================================

model2_result = model2.wv.most_similar(scent,topn=20)

result_list = []
for i in range(len(model2_result)):
  result_list.append(model2_result[i][0]+' '+str(np.round(model2_result[i][1], 2)))
scent_result = result_list[0].rsplit(' ',1)#오른쪽 기준으로 첫 번째 해당하는 sep 기준으로 분리

# '' 데이터 전처리 안돼서 코드란에서 거르기
if scent_result != '':
  scent_answer = scent_result[0]
else:
  scent_answer = scent_result[1]

x1 = accords_x1[scent]

st.write(f'위 노트가 사용된 향수의 갯수는 {x1}개 입니다.')
st.write(f'함께 사용된 향은 아래와 같습니다.')
col_p = ["향","유사도"]
pd_df = pd.DataFrame(model2_result, columns=col_p)

st.write(pd_df.head(20))
#============================향수 추천==============================
data = pd.read_csv('perfume.csv')
data['accords'].replace('', np.nan, inplace=True)
accords = data['accords'].dropna()

perfume_list = []
def perfum_title(scent):
  for i in range(51211):
    try:
      data_split = accords[i].split(',')
      for split_scent in data_split:
        if split_scent == scent:
          perfume_list.append(data['title'][i])
    except:
      pass
  return perfume_list
        
scent2 = perfum_title(scent)
st.write("선택한 노트가 들어간 향수를 볼 수 있습니다.")
# st.write(scent2[:10])

#=======================스트림릿 버튼========================
ss = SessionState.get(x=0)

def minus_clicks():
  if ss.x > 1:
    ss.x -= 1

def reset_clicks():
  ss.x = 0

if st.button("10개씩 보기"):
    ss.x = ss.x + 1
    if ss.x == 1:
      st.write(scent2[:10])
      st.write(f"현재 페이지는 {ss.x}페이지 입니다")
    elif ss.x > 1:
      try:
        st.write(scent2[(ss.x-1)*10:ss.x*10])
        st.write(f"현재 페이지는 {ss.x}페이지 입니다")
      except:
        pass

if ss.x >= 2:
  if st.button(label="이전 목록", on_click=minus_clicks):
    st.write(f"10개씩 보기를 누르면 {ss.x}페이지로 이동합니다")
    ss.x = ss.x - 1      

# st.button(label="이전 목록", on_click=minus_clicks)

#=====================스트림릿 리셋=======================
st.button(label = '1페이지로 이동', on_click=reset_clicks)


genre = st.sidebar.radio(
    "향수에 관심이 있으신가요??",
    ('향수에 관심 없어요!', '관심은 있는데 잘 모르겠어요', '네 알고싶어요!'))
if genre != '향수에 관심 없어요!':
  st.sidebar.write('이 사이트를 참고해보세요 => https://www.fragrantica.com/')
else:
  st.sidebar.title(" ;( ")