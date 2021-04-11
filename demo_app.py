import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objs as go
import seaborn as sns

with st.echo(code_location='below'):

    st.title("Netfix Movies and TVshows")
    st.write("Данный дэшборд направлен на ознакомление с информацией о фильмах и сериалах размещенных на платформе Netflix. Для получения информации о рейтингах были так же задействоавны данные с IMDb.")
    df = pd.read_csv("netflix_titles.csv")
    dg = pd.read_csv("IMDb ratings.csv")
    dh = pd.read_csv("IMDb movies.csv")
    idrate = dg[["imdb_title_id", "weighted_average_vote"]]
    idtitle = dh[["imdb_title_id", "title"]]
    tog = idtitle.merge(idrate)
    pog = df.merge(tog).drop_duplicates(subset='title')
    st.header("Укажи год, и узнаешь лучшие Movies or TVshows выпущенные в этом году, которые есть на нетфликсе")
    yearslist = pog["release_year"].tolist()
    newyearslist = []
    for i in yearslist:
        newyearslist.append(i)
    yearmin = min(newyearslist)
    yearmax = max(newyearslist)
    selectedyear = st.slider('Year', min_value=yearmin, max_value=yearmax)
    pog_filter = pog[pog["release_year"] == (selectedyear)]

    pog_filter_sorted = pog_filter.sort_values(by='weighted_average_vote', ascending=False)
    titrate = pog_filter_sorted[["title", 'weighted_average_vote']]
    toptitle = titrate['title'].tolist()[:10]
    toprate = titrate['weighted_average_vote'].tolist()[:10]

    a = np.array(toptitle)
    b = np.array(toprate)
    ###FROM: https://github.com/hupili/python-for-data-and-media-communication-gitbook/issues/118
    c = list(plt.cm.colors.cnames.keys())[10:20]
    ###END FROM

    st.title("Рейтинг топ 10 фильмов в зависимости от года выпуска.")
    st.write("Здесь вы можете выбрать год выпуска фильма в период от 1946 года до 2021(все имеющиеся актуальные данные на Netflix) и узнать наилучшие фильмы имеющиеся на "
             "этом сервисе.(лучше выбирать года попозже, а то старых фильмов там мало")
    fig, ax = plt.subplots()
    ax.bar(a, b, color=c, width=0.5)
    for item in ([ax.title, ax.xaxis.label] +
                 ax.get_xticklabels()):
        item.set_fontsize(3.5)
    st.pyplot(fig)

    pog['rawdur'] = pd.to_numeric(pog['duration'].apply(lambda x: x.split(" ", 1)[0]))

    ###FROM: https://www.youtube.com/watch?v=dwBkTbyHWY4
    data = [go.Scatter(
        x=pog['release_year'],
        y=pog['weighted_average_vote'],
        text=pog['title'],
        mode='markers',
        marker=dict(size=pog['rawdur'] / 10)
    )]
    layout = go.Layout(
        title='Все фильмы и сериалы имеющиеся на Netflix',
        xaxis=dict(title='Год выпуска'),
        yaxis=dict(title='Рейтинг'),
        hovermode='closest'
    )
    ###END FROM
    st.write("Перейдем к следующему графику.Во первых, чтобы было понятнее, размер шарика на графике показывает его длительность, распределены шарики в соотсветствии со своим годом выпуска и рейтингом. Чтобы узнать, конкретный период или инетерсующий вас разброс"
        " рейтинга, можно выделить область на графике и посмотреть в приближенном варианте." )
    fug = go.Figure(data=data, layout=layout)
    st.plotly_chart(fug)
    pog_indian = pog[pog["country"] == 'India']
    pog_world = pog[pog["country"] != 'India']
    st.write("По этому графику можем выделить несколько зависимостей")
    st.write("1) Можно заметить, что большинство фильмов сосредоточено ближе к текущему году, и старые фильмы с низким рейтингом также в большинстве своем отсутствуют. Это говорит о том, что политика Netflix ориентирована на современную молодежь")
    st.write("2) Также, можно заметить, что в среднем длительность фильмов упала к текущему году, это говорит о более высокой клиповости мышления у современной аудитории")

    st.title("Жанры и актеры")
    st.write(
        "В дальнейших данных я решил разделить индийский кинематограф и кинематограф остального мира для получения более адеквавтной выборки для целевой аудитории данного дэшборда"
        ", но если есть фанаты Индийского кино, то наслаждайтесь")
    which = st.multiselect('Выбери предпочитаемый кинематограф(Только один!!!)', ('Indian', 'Other world'))

    try:
        if which[0] == "Indian":
            cin = pog_indian
        else:
            cin = pog_world
    except IndexError:
        pass


    # ТОП ЖАНРОВ ПО КОЛИЧЕСТВУ ИСПОЛЬЗОВАНИЙ
    def genres(inworld):
        genr = inworld['listed_in'].dropna().tolist()
        genrlist = []
        for i in genr:
            genre = i.split(',')
            for j in genre:
                genrlist.append(j.strip(' '))
        counter = []
        for k in genrlist:
            cunter = genrlist.count(k)
            counter.append(cunter)
        return genrlist, counter


    try:
        bestgenres = dict(zip(genres(cin)[0], genres(cin)[1]))
        bestgenres1 = sorted(bestgenres.values(), reverse=True)
        sortedbestgenres1 = {}
    except  NameError:
        pass


    # ТОП АКТЕРОВ ПО КОЛИЧЕСТВУ ПОЯВЛЕНИЙ В ФИЛЬМАХ
    def topactors(inworld):
        actors = inworld["cast"].dropna().tolist()

        bigactorslist = []
        for i in actors:
            actorslist = i.split(',')
            for j in actorslist:
                bigactorslist.append(j.strip(' '))

        counter = []
        for uwu in bigactorslist:
            cunter = bigactorslist.count(uwu)
            counter.append(cunter)
        return bigactorslist, counter


    try:
        coolactors = dict(zip(topactors(cin)[0], topactors(cin)[1]))
        coolactors1 = sorted(coolactors.values(), reverse=True)
        sortedcoolactors1 = {}
    except NameError:
        pass


    # делает вещи
    @st.cache
    def col(q, w, e):
        for i in w:
            for k in q.keys():
                if q[k] == i:
                    e[k] = q[k]
        return (e)


    try:
        datagenre = pd.DataFrame.from_dict(col(bestgenres, bestgenres1, sortedbestgenres1), orient='index',
                                           columns=["Movies with this genre"])
    except NameError:
        pass
    try:
        pogchamp = pd.DataFrame.from_dict(col(coolactors, coolactors1, sortedcoolactors1), orient='index',
                                          columns=['Times in movie'])
    except NameError:
        pass
    # ХУДОЖЕСТВЕННЫЙ ФИЛЬМ СПИЗДИЛИ
    # st.write(datagenre)
    fig1, ax1 = plt.subplots()

    exlist = (0.2, 0.1, 0, 0, 0, 0, 0, 0, 0, 0)

    try:
        patches, texts = ax1.pie(datagenre['Movies with this genre'].tolist()[:10], colors=c, startangle=90,
                                 explode=exlist, shadow=True)
        for text in texts:
            text.set_color('black')
        ax1.axis('equal')
        plt.legend(labels=datagenre.index, loc='upper right', facecolor='white')
        plt.tight_layout()
        st.pyplot(fig1)
    except NameError:
        pass
    st.title("Для тех, кому интересно какие актеры сыграли в наибольшем количестве фильмов на Netflix можете глянуть, они также разделены на индусов и остальнйо мир")
    sns.set(font_scale=1)
    f2, ax = plt.subplots(figsize=(10, 30))
    colors_cw = sns.color_palette('magma', len(pogchamp['Times in movie'].tolist()))
    sns.barplot(pogchamp.index, pogchamp['Times in movie'], palette=colors_cw[::-1])
    Text = ax.set(xlabel='nya ichi ni san', title='nya arigato')
    st.pyplot(f2)
    if st.checkbox('Данные по жанрам'):
        st.write(datagenre)
    if st.checkbox("Данные по актерам"):
        st.write(pogchamp)
    if st.checkbox("Просто исходные данные"):
        st.write(pog)










