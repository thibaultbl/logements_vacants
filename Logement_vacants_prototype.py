
# coding: utf-8

# In[1]:


import pandas as pd
import os
import folium


PATH_DATA = "/home/thibault/Documents/Logements_vacants/Data/"


# In[2]:


def load_and_feature_enginerring(filename, aggregate=True, by="cd_dep"):
    data = pd.read_csv(filename,
                      sep=";")
    data.columns = ["iris_2015",
               "libiris",
               "com",
               "libcom",
               "cd_dep",
               "nb_logement_2013",
               "nb_residence_principale_2013",
               "nb_residence_secondaire_2013",
               "nb_logement_vacant_2013"]
    
    if aggregate:
        data =            data.groupby(by)["nb_logement_2013",
                                   "nb_residence_principale_2013",
                                   "nb_residence_secondaire_2013",
                                   "nb_logement_vacant_2013"].sum().reset_index()
    
    data.loc[:, "percent_logement_vacant"] =        (data.nb_logement_vacant_2013 / data.nb_logement_2013)
    return(data)


# ###### Map Départements

# In[3]:


data_departement =    load_and_feature_enginerring(PATH_DATA + 
                                 "base_logements-France-IRIS-2013_Global_Map_Solution_source_INSEE.csv")


# In[4]:


state_geo = os.path.join('data', PATH_DATA + 'departements.geojson')
m = folium.Map(location=[46.15, 2.06], zoom_start=5)

m.choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=data_departement,
    columns=['cd_dep', 'percent_logement_vacant'],
    key_on='feature.properties.code',
    fill_color='YlGn',
    fill_opacity=1,
    line_opacity=0.5,
    legend_name='Logements vacants (%)'
)


#folium.LayerControl().add_to(m)

m


# ###### Map commune

# In[3]:


data_commune =    load_and_feature_enginerring(PATH_DATA + 
                                 "base_logements-France-IRIS-2013_Global_Map_Solution_source_INSEE.csv",
                                aggregate=True, by="com")


# In[4]:


state_geo = os.path.join('data', PATH_DATA + 'communes.geojson')
m = folium.Map(location=[46.15, 2.06], zoom_start=5)

m.choropleth(
    geo_data=state_geo,
    name='choropleth',
    data=data_commune,
    columns=['com', 'percent_logement_vacant'],
    key_on='feature.properties.code',
    fill_color='YlGn',
    fill_opacity=1,
    line_opacity=0.5,
    legend_name='Logements vacants (%)'
)

#folium.LayerControl().add_to(m)

m


# ###### Predict percent of inocupied logement
