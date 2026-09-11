import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. НАСТРОЙКА СТРАНИЦЫ
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write(
    "2026년 영화들의 날짜별 일관객 변화를 "
    "인터랙티브 그래프로 확인합니다."
)


# ============================================================
# 2. ДАННЫЕ
# ============================================================

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/"
    "modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():

    # CSV 파일을 인터넷에서 불러옵니다.
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환합니다.
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 데이터를 숫자형으로 변환합니다.
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


# ============================================================
# 3. ДАННЫЕ ЗАГРУЗКА
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error("데이터를 불러오지 못했습니다.")

    st.write(
        "인터넷 연결 또는 데이터 주소를 확인해 주세요."
    )

    st.stop()


# 데이터가 없는 경우
if df.empty:

    st.warning("데이터가 없습니다.")

    st.stop()


# ============================================================
# 4. 2026년 데이터만 사용
# ============================================================

df_2026 = df[
    df["날짜"].dt.year == 2026
].copy()


if df_2026.empty:

    st.warning(
        "2026년 데이터가 없습니다."
    )

    st.stop()


# ============================================================
# 5. 그래프 제목
# ============================================================

st.divider()

st.header("📈 그래프 1 — 2026년 영화별 일관객 변화")

st.write(
    "여러 영화를 선택하면 같은 그래프에서 "
    "시간에 따른 관객수 변화를 비교할 수 있습니다."
)


# ============================================================
# 6. 영화 선택
# ============================================================

movie_list = sorted(
    df_2026["영화명"]
    .dropna()
    .unique()
    .tolist()
)


# 2026년에 존재하는 영화 이름 확인
default_movies = []

for movie in [
    "오디세이",
    "스파이더맨: 브랜드 뉴 데이"
]:

    if movie in movie_list:
        default_movies.append(movie)


# 영화 선택
selected_movies = st.multiselect(
    "비교할 영화를 선택하세요.",
    options=movie_list,
    default=default_movies
)


# ============================================================
# 7. 선택된 영화 데이터
# ============================================================

if len(selected_movies) == 0:

    st.info(
        "위에서 영화를 한 편 이상 선택해 주세요."
    )

    st.stop()


selected_df = df_2026[
    df_2026["영화명"].isin(selected_movies)
].copy()


# 날짜순 정렬
selected_df = selected_df.sort_values(
    ["날짜", "영화명"]
)


# ============================================================
# 8. LINE GRAPH
# ============================================================

fig = px.line(
    selected_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="2026년 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객수",
        "영화명": "영화"
    }
)


# ★ 중요:
# 점만 보이는 것이 아니라 선으로 연결합니다.
fig.update_traces(
    mode="lines+markers",
    connectgaps=True,
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)


fig.update_layout(

    height=650,

    hovermode="x unified",

    xaxis=dict(
        title="날짜",
        type="date"
    ),

    yaxis=dict(
        title="일관객수",
        tickformat=","
    ),

    legend=dict(
        title="영화"
    )
)


# 그래프 표시
st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 9. 그래프에서 알 수 있는 것
# ============================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "직접 설명을 작성하세요.",
    value="",
    placeholder=(
        "예: 영화의 개봉 직후 관객수가 가장 높고 "
        "시간이 지나면서 감소하는 경향을 보인다."
    ),
    height=120
)


# ============================================================
# 10. 데이터 정보
# ============================================================

st.divider()

st.subheader("📊 현재 그래프의 데이터")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "데이터 시작일",
        df_2026["날짜"].min().strftime("%Y-%m-%d")
    )

with col2:
    st.metric(
        "데이터 마지막 날짜",
        df_2026["날짜"].max().strftime("%Y-%m-%d")
    )

with col3:
    st.metric(
        "영화 종류",
        f"{df_2026['영화명'].nunique():,}편"
    )


# ============================================================
# 11. 원본 데이터
# ============================================================

with st.expander("📋 원본 데이터 보기"):

    st.dataframe(
        selected_df,
        use_container_width=True
    )


# ============================================================
# 12. 다음 그래프 추가 공간
# ============================================================

st.divider()

st.header("📊 그래프 2")

st.info(
    "다음 그래프를 여기에 추가할 수 있습니다."
)
