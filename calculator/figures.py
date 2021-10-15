from . import plotly_app

df = px.data.gapminder()
fig = px.area(df, x="year", y="pop", color="continent", line_group="country")

fig.show()