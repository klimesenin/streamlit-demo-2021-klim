import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objs as go


with st.echo(code_location='below'):

    st.title("Netfix Movies and TVshows")
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
    c = list(plt.cm.colors.cnames.keys())[:10]
    # СПИЗЖЕНО
    #n = toptitle.__len__() + 1
    #all_colors = list(plt.cm.colors.cnames.keys())
    #c = random.choices(all_colors, k=n)
    # ЗАКОНЧИЛ ПИЗДИТЬ
    fig, ax = plt.subplots()
    ax.bar(a, b, color=c, width=0.5)
    for item in ([ax.title, ax.xaxis.label] +
                 ax.get_xticklabels()):
        item.set_fontsize(3.5)
    st.pyplot(fig)

    pog['rawdur'] = pd.to_numeric(pog['duration'].apply(lambda x: x.split(" ", 1)[0]))

    # спизжено
    data = [go.Scatter(
        x=pog['release_year'],
        y=pog['weighted_average_vote'],
        text=pog['title'],
        mode='markers',
        marker=dict(size=pog['rawdur'] / 10)
    )]
    layout = go.Layout(
        title='year vs rating, размер шарика в зависимости от длительности фильма',
        xaxis=dict(title='Year'),
        yaxis=dict(title='rating'),
        hovermode='closest'
    )
    #
    fug = go.Figure(data=data, layout=layout)
    st.plotly_chart(fug)
    pog_indian = pog[pog["country"] == 'India']
    pog_world = pog[pog["country"] != 'India']
    st.write(
        "В данном датасете я разделю индийский кинематограф и кинематограф остального мира для получения более нормальных результатов")
    which = st.multiselect('Select which cinematography do you prefer(SELECT ONLY ONE!):', ('Indian', 'Other world'))

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

    st.write(pog)
    if st.checkbox('дата жанров'):
        st.write(datagenre)
    if st.checkbox("Если хочется raw data, DATA TOPACTORS"):
        st.write(pogchamp)
    if st.checkbox("Нажми сюда и я покажу тебе данные бро (raw data)"):
        st.write(pog)










