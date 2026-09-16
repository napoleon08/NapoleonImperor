import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 1. НАСТРОЙКА СТРАНИЦЫ
# ============================================================

st.set_page_config(
    page_title="2026 Korea Movie Data",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 2026 한국 영화 데이터 그래프")

st.subheader(
    "The Most Popular Movies in Korea — 2026"
)

st.write(
    "2026년 한국 박스오피스에서 가장 많은 관객을 기록한 "
    "영화들의 일별 관객수, 누적관객수와 순위 변화를 분석합니다."
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

    df = pd.read_csv(DATA_URL)

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자 데이터 변환
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

    return df


# ============================================================
# 3. ЗАГРУЗКА
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "영화 데이터를 불러오지 못했습니다."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# 4. 2026 ДАННЫЕ
# ============================================================

df_2026 = df[
    df["날짜"].dt.year == 2026
].copy()


if df_2026.empty:

    st.error(
        "2026년 데이터가 없습니다."
    )

    st.stop()


# ============================================================
# 5. САМЫЕ ПОПУЛЯРНЫЕ ФИЛЬМЫ
# ============================================================

popular_movies = [
    "왕과 사는 남자",
    "오디세이",
    "스파이더맨: 브랜드 뉴 데이",
    "군체",
    "호프"
]


# ============================================================
# 6. ПРОВЕРЯЕМ, КАКИЕ ФИЛЬМЫ ЕСТЬ В CSV
# ============================================================

available_movies = []

for movie in popular_movies:

    if movie in df_2026["영화명"].unique():

        available_movies.append(movie)


# ============================================================
# 7. ЕСЛИ НЕКОТОРЫХ НЕТ — ПОКАЗЫВАЕМ СООБЩЕНИЕ
# ============================================================

missing_movies = [
    movie
    for movie in popular_movies
    if movie not in available_movies
]


if missing_movies:

    st.warning(
        "일부 영화의 제목이 데이터에서 발견되지 않았습니다."
    )

    st.write(
        "찾지 못한 영화:",
        missing_movies
    )


if len(available_movies) == 0:

    st.error(
        "선택한 인기 영화가 데이터에 없습니다."
    )

    st.stop()


# ============================================================
# 8. ВЫБОР ФИЛЬМОВ
# ============================================================

st.divider()

st.header(
    "🎬 인기 영화 선택"
)

selected_movies = st.multiselect(
    "그래프에 표시할 영화를 선택하세요.",
    options=available_movies,
    default=available_movies
)


if len(selected_movies) == 0:

    st.info(
        "영화를 한 편 이상 선택하세요."
    )

    st.stop()


selected_df = df_2026[
    df_2026["영화명"].isin(selected_movies)
].copy()


selected_df = selected_df.sort_values(
    ["날짜", "영화명"]
)


# ============================================================
# 9. ГРАФИК 1 — ЕЖЕДНЕВНАЯ ПОСЕЩАЕМОСТЬ
# ============================================================

st.divider()

st.header(
    "📈 그래프 1 — 일별 관객수"
)

st.write(
    "각 영화가 날짜별로 몇 명의 관객을 모았는지 보여줍니다."
)


fig1 = px.line(
    selected_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="Daily Audience — 2026",
    labels={
        "날짜": "날짜",
        "일관객": "일 관객수",
        "영화명": "영화"
    }
)


fig1.update_traces(
    mode="lines+markers",
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "일 관객수: %{y:,}명"
        "<extra></extra>"
    )
)


fig1.update_layout(
    height=650,
    hovermode="x unified",
    xaxis=dict(
        title="날짜"
    ),
    yaxis=dict(
        title="일 관객수",
        tickformat=","
    )
)


st.plotly_chart(
    fig1,
    use_container_width=True
)


# ============================================================
# 10. ЧТО МОЖНО УЗНАТЬ
# ============================================================

st.subheader(
    "💡 이 그래프로 알 수 있는 것"
)

st.text_area(
    "직접 설명을 작성하세요.",
    placeholder=(
        "예: 영화의 개봉 직후 관객수가 급격히 증가한 후 "
        "시간이 지나면서 감소하는 모습을 볼 수 있다."
    ),
    height=110
)


# ============================================================
# 11. ГРАФИК 2 — НАКОПИТЕЛЬНАЯ ПОСЕЩАЕМОСТЬ
# ============================================================

st.divider()

st.header(
    "📊 그래프 2 — 누적 관객수"
)

st.write(
    "각 영화의 누적 관객수가 시간에 따라 "
    "어떻게 증가했는지 보여줍니다."
)


fig2 = px.line(
    selected_df,
    x="날짜",
    y="누적관객",
    color="영화명",
    markers=True,
    title="Cumulative Audience — 2026",
    labels={
        "날짜": "날짜",
        "누적관객": "누적 관객수",
        "영화명": "영화"
    }
)


fig2.update_traces(
    mode="lines+markers",
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "누적 관객수: %{y:,}명"
        "<extra></extra>"
    )
)


fig2.update_layout(
    height=650,
    hovermode="x unified",
    xaxis=dict(
        title="날짜"
    ),
    yaxis=dict(
        title="누적 관객수",
        tickformat=","
    )
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# ============================================================
# 12. ЧТО МОЖНО УЗНАТЬ
# ============================================================

st.subheader(
    "💡 이 그래프로 알 수 있는 것"
)

st.text_area(
    "직접 설명을 작성하세요.",
    placeholder=(
        "예: 누적 관객수가 가장 빠르게 증가한 영화가 "
        "가장 강한 흥행을 기록한 영화라고 볼 수 있다."
    ),
    height=110
)


# ============================================================
# 13. ГРАФИК 3 — РЕЙТИНГ
# ============================================================

st.divider()

st.header(
    "🏆 그래프 3 — 일별 박스오피스 순위"
)

st.write(
    "각 영화의 일별 박스오피스 순위가 "
    "시간에 따라 어떻게 변했는지 보여줍니다."
)


fig3 = px.line(
    selected_df,
    x="날짜",
    y="순위",
    color="영화명",
    markers=True,
    title="Daily Box Office Ranking — 2026",
    labels={
        "날짜": "날짜",
        "순위": "박스오피스 순위",
        "영화명": "영화"
    }
)


fig3.update_traces(
    mode="lines+markers",
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "순위: %{y}위"
        "<extra></extra>"
    )
)


# Рейтинг: 1 место должно быть сверху
fig3.update_yaxes(
    autorange="reversed",
    dtick=1
)


fig3.update_layout(
    height=650,
    hovermode="x unified",
    xaxis=dict(
        title="날짜"
    ),
    yaxis=dict(
        title="박스오피스 순위"
    )
)


st.plotly_chart(
    fig3,
    use_container_width=True
)

# ============================================================
# 13. 그래프 4 — TOP 10 영화
# ============================================================

st.divider()

st.header(
    "🏆 그래프 4 — 기간별 관객수 TOP 10"
)

st.write(
    "선택한 기간 동안 각 영화의 일관객을 모두 합산하여 "
    "관객수가 가장 많은 영화 TOP 10을 보여줍니다."
)


# 영화별 총 관객수 계산
top10_movies = (
    df_2026
    .groupby("영화명")
    .agg(
        총관객수=("일관객", "sum"),
        TOP10_진입일수=("날짜", "nunique")
    )
    .reset_index()
)


# 총 관객수가 많은 순서로 정렬
top10_movies = (
    top10_movies
    .sort_values(
        "총관객수",
        ascending=False
    )
    .head(10)
)


# 그래프용 데이터는 관객수가 많은 영화가 위에 오도록
top10_movies = top10_movies.sort_values(
    "총관객수",
    ascending=True
)


fig4 = px.bar(
    top10_movies,
    x="총관객수",
    y="영화명",
    orientation="h",
    text="총관객수",
    title="선택한 기간 영화별 누적 일관객 TOP 10",
    labels={
        "총관객수": "기간 내 총 관객수",
        "영화명": "영화"
    }
)


fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "기간 내 총 관객수: %{x:,}명<br>"
        "TOP 10 진입일수: %{customdata}일"
        "<extra></extra>"
    ),
    customdata=top10_movies[
        ["TOP10_진입일수"]
    ]
)


fig4.update_layout(
    height=650,
    xaxis=dict(
        title="기간 내 총 관객수",
        tickformat=","
    ),
    yaxis=dict(
        title="영화",
        categoryorder="total ascending"
    )
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader(
    "💡 이 그래프로 알 수 있는 것"
)

st.text_area(
    "직접 설명을 작성하세요.",
    placeholder=(
        "예: 선택한 기간 동안 일관객의 합이 가장 높은 영화와 "
        "10위권에 오래 머문 영화를 확인할 수 있다."
    ),
    height=110
)

# ============================================================
# 14. ОБЩИЙ АНАЛИЗ
# ============================================================

st.divider()

st.header(
    "🧠 종합 분석"
)

st.write(
    "세 그래프를 비교하여 영화의 흥행 과정을 분석해 보세요."
)


st.text_area(
    "직접 분석을 작성하세요.",
    placeholder=(
        "예: 일 관객수와 누적 관객수 그래프를 비교하면 "
        "개봉 초기 흥행이 강했던 영화를 확인할 수 있다. "
        "또한 순위 그래프를 통해 영화의 흥행 순위가 "
        "시간에 따라 어떻게 변화했는지 알 수 있다."
    ),
    height=160
)


# ============================================================
# 15. ФИНАЛЬНЫЕ ПОКАЗАТЕЛИ
# ============================================================

st.divider()

st.header(
    "📊 현재 선택된 영화 데이터"
)


for movie in selected_movies:

    movie_df = selected_df[
        selected_df["영화명"] == movie
    ].copy()

    if movie_df.empty:
        continue

    max_cumulative = movie_df[
        "누적관객"
    ].max()

    best_rank = movie_df[
        "순위"
    ].min()

    st.write(
        f"### 🎬 {movie}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "최대 누적 관객수",
            f"{max_cumulative:,.0f}명"
        )

    with col2:

        st.metric(
            "최고 순위",
            f"{int(best_rank)}위"
        )


# ============================================================
# 16. ИСХОДНЫЕ ДАННЫЕ
# ============================================================

st.divider()

with st.expander(
    "📋 원본 데이터 보기"
):

    st.dataframe(
        selected_df,
        use_container_width=True
    )


# ============================================================
# 17. ИСТОЧНИК
# ============================================================

st.divider()

st.subheader(
    "📚 데이터 출처"
)

st.write(
    "KOBIS / KOBIZ — Korean Box Office Information System"
)

st.write(
    "분석 대상: 2026년 인기 영화"
)

st.write(
    "영화: 왕과 사는 남자, 오디세이, "
    "스파이더맨: 브랜드 뉴 데이, 군체, 호프"
)


st.success(
    "2026년 인기 영화 3개 그래프 분석이 완료되었습니다! 🎬"
)
