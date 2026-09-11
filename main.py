import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "1년치 일별 박스오피스 데이터를 이용하여 "
    "영화의 시간에 따른 관객수 변화를 살펴봅니다."
)


# ============================================================
# 2. 데이터 불러오기 및 전처리
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # CSV 파일을 인터넷에서 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환합니다.
    # 원래 날짜는 20260101과 같은 8자리 숫자입니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자 열을 숫자형으로 변환합니다.
    number_columns = [
        "순위",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in number_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # 날짜순으로 정렬합니다.
    df = df.sort_values("날짜")

    return df


# 데이터 불러오기
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 데 문제가 발생했습니다.")
    st.info(
        "인터넷 연결과 데이터 주소를 확인해 주세요."
    )
    st.stop()


# 데이터가 비어 있는지 확인
if df.empty:
    st.warning("불러온 데이터가 없습니다.")
    st.stop()


# ============================================================
# 3. 그래프 1 — 시간에 따른 일관객 변화
# ============================================================

st.divider()

st.header("📈 그래프 1 — 시간에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)


# 영화 목록 만들기
movie_list = sorted(
    df["영화명"].dropna().unique().tolist()
)


if len(movie_list) == 0:

    st.warning("선택할 영화가 없습니다.")
    st.stop()


# 영화 선택 드롭다운
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)


# 선택한 영화만 필터링
movie_df = df[
    df["영화명"] == selected_movie
].copy()


# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# ============================================================
# 4. 인터랙티브 선 그래프
# ============================================================

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie} — 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객수"
    }
)


# 마우스를 그래프 위에 올렸을 때
# 날짜와 관객수가 표시되도록 설정합니다.
fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "관객수: %{y:,}명"
    "<extra></extra>"
)


fig.update_layout(
    hovermode="x unified",
    height=550
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 5. 그래프에서 알 수 있는 것
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

# 이 문장은 사용자가 직접 작성할 수 있습니다.
explanation = st.text_area(
    "설명 문장을 직접 작성하세요.",
    value="여기에 이 그래프로 알 수 있는 내용을 작성하세요.",
    height=100,
    key="graph1_explanation"
)

st.caption(
    "※ 이 부분은 직접 작성해서 사용할 수 있습니다."
)


# ============================================================
# 6. 다음 그래프를 추가할 공간
# ============================================================

st.divider()

st.header("📊 그래프 2")

st.info(
    "앞으로 새로운 그래프를 이곳에 추가할 수 있습니다."
)

# 예:
# - 영화별 누적관객 비교
# - 날짜별 전체 관객수 변화
# - 스크린수와 관객수의 관계
# - 상영횟수와 관객수의 관계


# ============================================================
# 7. 데이터 확인
# ============================================================

with st.expander("📋 원본 데이터 일부 보기"):

    st.dataframe(
        df.head(20),
        use_container_width=True
    )
