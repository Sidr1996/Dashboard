import  pandas as pd
import numpy as np
import plotly.express as px
import prince
# import gspread
import pandas as pd

data2=pd.read_excel("opendata_COD_cause (1).xlsx")

data2=data2.iloc[:,[0,2,3,4,5,6,7,8]]
data2.columns=["CD_maladie","Cause","CD_Region","Month","Year","Age","Genre","Total"]
data_2=pd.DataFrame(data2.values.repeat(data2["Total"], axis=0), columns=data2.columns)
data2['Year']=data2['Year'].astype('category')
data2["CD_Region"]=data2["CD_Region"].astype('category')
data2["Age"]=data2["Age"].astype('category')
data2["CD_Region"]= data2["CD_Region"] .cat.rename_categories(["Region_Flamande",
"Region Wallonne","Region_Brux_Capit"])

data_2['Year']=data_2['Year'].astype('category')
data_2["CD_Region"]=data_2["CD_Region"].astype('category')
data_2["Age"]=data_2["Age"].astype('category')

data_2["CD_Region"]= data_2["CD_Region"] .cat.rename_categories(["Region_Flamande",
"Region Wallonne","Region_Brux_Capit"])

def data_brut():
    return data2

maladies=data2.groupby("Cause").sum()
maladies["Cause"]=maladies.index
maladies=maladies.sort_values(by=["Total"])
#fig=px.bar(maladies,x='Total',y="Cause", title="Cause de Décès",text_auto='.8s', height=600)

def fig_cause_dece():
    fig=px.bar(maladies,x='Total',y="Cause", title="Cause de Décès", height=600)
    return fig



maladies2=data2.groupby(["Cause","Year"]).sum()
maladies2.reset_index(inplace=True)

#fig2=px.line(maladies2,x="Year", y="Total", color="Cause", title="")
#fig2

def fig_cause_year():
    fig=px.line(maladies2,x="Year", y="Total", color="Cause", title="Evolution des causes par ans")
    return fig


maladies3=data2.groupby(["Age","Genre"]).sum()
maladies3.reset_index(inplace=True)
def fig_age_genre(nom="Age"):
    fig=px.pie(maladies3,values="Total", names=nom, hole=.7)
    return fig

maladies4=data2.groupby(["Age","Genre"]).sum()
maladies4.reset_index(inplace=True)
#fig3=px.bar(maladies4, x="Age", y="Total", color="Genre",barmode="group", width=500)

def fig_ag():
    fig=px.bar(maladies4, x="Age", y="Total", color="Genre",barmode="group", width=500, title="Graphique Age vs Genre")
    return fig


data3=data2
region_2=data3.groupby(["Cause","CD_Region"]).sum()
region_2.reset_index(inplace=True)
# fig7=px.bar(region_2, x="Cause", y="Total", color="CD_Region",barmode="group", height=800,color_discrete_map={
#                 "Region_Flamande": "red",
#                 "Region Wallonne": "green",
#                 "Region_Brux_Capit": "goldenrod",})
data4=data2
region_3=data4.groupby(["CD_Region","Year"]).sum()
region_3.reset_index(inplace=True)
#fig8=px.line(region_3, x='Year',y='Total', color="CD_Region")


def fig_ultimo_dopddown(optiones="Cause-CD_Region"):
    if optiones=="Cause-CD_Region":
        fig7=px.bar(region_2, x="Cause", y="Total", color="CD_Region",barmode="group", title="Cuases vs Region",height=800,color_discrete_map={
                "Region_Flamande": "red",
                "Region Wallonne": "green",
                "Region_Brux_Capit": "goldenrod",})
        return fig7
    elif optiones=="CD_Region-Year":
        fig9=px.line(region_3, x='Year',y='Total', color="CD_Region")
        return fig9







a=data_2[["Genre","Age","Cause","CD_Region"]]
ca= prince.MCA(n_components=2,
n_iter=3,copy=True,check_input=True,engine='auto',random_state=42)



ca = ca.fit(a)
cordonnees=ca.column_coordinates(a)

cordonnees["masa"]=ca.col_masses_

cordonnees["categories"]=cordonnees.index


type_cordonnees=[]
for i in cordonnees["categories"]:
    if  "Genre" in i:
        type_cordonnees.append("Genre")
    elif "Age"  in i:
        type_cordonnees.append("Age")
    elif "Cause" in i:
        type_cordonnees.append("Cause")
    elif "CD_Region" in i:
        type_cordonnees.append("Region")


cordonnees["Type"]=type_cordonnees

cordonnees.columns=["cord_x","cord_y","masa","categories","type_cat"]
cordonnees=cordonnees.drop("Cause_Codes d'utilisation particulière")
cordonnees=cordonnees.round(2)

def ACM_graph():
    fig4= px.scatter(cordonnees, x="cord_x", y="cord_y", color="type_cat",
                 hover_name="categories", size_max=60, title='Analyse de Correspondance Multiple' )
    fig4.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    fig4.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    return fig4


b=data_2[["Age","Cause"]]
cb= prince.MCA(n_components=2,
n_iter=3,copy=True,check_input=True,engine='auto',random_state=42)



cb = cb.fit(b)
cordonneesb=cb.column_coordinates(b)

cordonneesb["masa"]=cb.col_masses_

cordonneesb["categories"]=cordonneesb.index


type_cordonneesb=[]
for i in cordonneesb["categories"]:
    if  "Genre" in i:
        type_cordonneesb.append("Genre")
    elif "Age"  in i:
        type_cordonneesb.append("Age")
    elif "Cause" in i:
        type_cordonneesb.append("Cause")
    elif "CD_Region" in i:
        type_cordonneesb.append("Region")


cordonneesb["Type"]=type_cordonneesb

cordonneesb.columns=["cord_x","cord_y","masa","categories","type_cat"]
cordonneesb=cordonneesb.drop("Cause_Codes d'utilisation particulière")
cordonneesb=cordonneesb.round(2)

def ACS_age_cause():
    fig5 = px.scatter(cordonneesb, x="cord_x", y="cord_y", color="type_cat",
                 hover_name="categories", size_max=60,title='Analyse de Correspondance Simple Age-Cause' ,width=500)
    fig5.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    fig5.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    return fig5


c=data_2[["Genre","Cause"]]
cb= prince.MCA(n_components=2,
n_iter=3,copy=True,check_input=True,engine='auto',random_state=42)



cc = cb.fit(c)
cordonneesc=cb.column_coordinates(c)

cordonneesc["masa"]=cc.col_masses_

cordonneesc["categories"]=cordonneesc.index


type_cordonneesc=[]
for i in cordonneesc["categories"]:
    if  "Genre" in i:
        type_cordonneesc.append("Genre")
    elif "Age"  in i:
        type_cordonneesc.append("Age")
    elif "Cause" in i:
        type_cordonneesc.append("Cause")
    elif "CD_Region" in i:
        type_cordonneesc.append("Region")


cordonneesc["Type"]=type_cordonneesc

cordonneesc.columns=["cord_x","cord_y","masa","categories","type_cat"]
cordonneesc=cordonneesc.drop("Cause_Codes d'utilisation particulière")
cordonneesc=cordonneesc.round(2)


def ACS_genre_cause():
    fig6 = px.scatter(cordonneesc, x="cord_x", y="cord_y", color="type_cat",
                 hover_name="categories", size_max=60,title='Analyse de Correspondance Simple Genre-Cause',width=500 )
    fig6.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    fig6.update_yaxes(zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    return fig6

