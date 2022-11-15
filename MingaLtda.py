import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import locale
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
#locale.setlocale(locale.LC_TIME, 'es_EC.UTF-8')

def main():
    pass
if __name__ == '__main__':
    main()


#st.set_page_config(page_title = 'Riesgo Operativo', layout='wide')
#st.title('MINGA LTDA. DASHBOARD - Riesgo Operativo')
#st.markdown('**COAC MINGA LTDA.**')
#st.markdown("____")

col1,col2,col3 = st.columns((2,3,1))
col2.markdown('### DASHBOARD PRINCIPAL') 


def nivel_riesgo_color(nivel_riesgo_inherente_sc):
    bgcolor = 'grey'
    if nivel_riesgo_inherente_sc == 'MUY BAJO':
        bgcolor = '#79b36b'#verdeoscuro
    if nivel_riesgo_inherente_sc == 'BAJO':
        bgcolor = '#adff99'#verde
    if nivel_riesgo_inherente_sc == 'MEDIO':
        bgcolor = '#ffff99'#amarillo
    if nivel_riesgo_inherente_sc == 'ALTO':
        bgcolor = '#ffce99'#naranja
    if nivel_riesgo_inherente_sc == 'CRÍTICO':
        bgcolor = '#ff9999'#rojo
    return f'color: black; background-color: {bgcolor}'

def riesgo_color(calif_riesgo_inherente_sc):
    bgcolor = '#79b36b'
    if 0 < calif_riesgo_inherente_sc <= 5:
        bgcolor = '#79b36b'#verdeoscuro
    if 5 < calif_riesgo_inherente_sc <= 10:
        bgcolor = '#adff99'#verde
    if 10 < calif_riesgo_inherente_sc <= 15:
        bgcolor = '#ffff99'#amarillo
    if 15 < calif_riesgo_inherente_sc <= 20:
        bgcolor = '#ffce99'#naranja
    if calif_riesgo_inherente_sc > 20:
        bgcolor = '#ff9999'#rojo
    return f'color: grey; background-color: {bgcolor}'

### PARA TRANSFORMAR LA HOJA rop1_idclascalif5x5 EN EL DATAFRAME df1_matrizrop
matrizrop = pd.ExcelFile('rop_minga.xlsx')
df1_matrizrop = matrizrop.parse('identific_riesgos')
df1_matrizrop['fecha_identificacion'] = pd.to_datetime(df1_matrizrop["fecha_identificacion"], errors='coerce').dt.strftime('%b/%y')
df1_matrizrop['fecha'] = df1_matrizrop['fecha_identificacion']
## COLUMNAS EN DATAFRAME df1_matrizrop
# fecha_identificacion
# id_riesgo
# descripcion_riesgo
# factor_causal
# efecto_inmediato_potencial_mayor
# tipo_efecto_inmediato
# tep_n3
# tep_n2
# tep_n1
# proceso
# macroproceso
# gerencia
# linea_negocio
# calif_impacto
# nivel_impacto
# calif_frecuencia
# nivel_frecuencia
# calif_riesgo_inherente_sc
# nivel_riesgo_inherente_sc
# calif_riesgo_inherente_cc
# nivel_riesgo_inherente_cc
# calif_riesgo_residual_enero
# nivel_riesgo_inherente_enero
# calif_riesgo_residual_febrero
# nivel_riesgo_inherente_febrero
# calif_riesgo_residual_marzo
# nivel_riesgo_inherente_marzo


### PARA CONSTRUIR EL df2_matrizresumen
df2_matrizresumen = df1_matrizrop[['fecha','descripcion_riesgo','nivel_riesgo_inherente_cc','factor_causal','tep_n1','proceso']]
df2_matrizresumen = df2_matrizresumen.style.applymap(nivel_riesgo_color, subset=['nivel_riesgo_inherente_cc'])
#st.write(df2_matrizresumen)

### PARA CONTRUIR LAS ETIQUETAS NUMÉRICAS
#col1, col2, col3, col4, col5 ,col6, col7 = st.columns(7)
#cant_riesgos = len(df2_matrizresumen.index)
#col1.write('')
#col2.metric(label="RIESGOS REGISTRADOS", value=cant_riesgos)
#col3.metric(label="EVENTOS REGISTRADOS", value="126")
#col4.metric(label="PLANES DE TRATAMIENTO", value="25")
#col5.metric(label="EVENTOS DE ESTE MES", value="33")
#col6.metric(label="PLANES COMPLETADOS", value="16")
#col7.write('')

### PARA LA MATRIZ DE ROP
with st.expander('Matriz de Riesgo Operativo Cualitativo'):
    st.write(df2_matrizresumen)

st.markdown("____")

col1,colm,col2 = st.columns((1,3,1))
with colm:
    st.markdown("**Wordcloud de riesgos descritos**")
    text = " ".join(i for i in df1_matrizrop.descripcion_riesgo)
    stopwords = set(stopwords.words('spanish', 'english')) 
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    figAA = plt.figure( figsize=(15,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.write(figAA)
st.markdown("____")
col1,colm,col2 = st.columns((1,0.1,1))
with col1:
    df3_fig3 = df1_matrizrop[['calif_impacto','calif_frecuencia','calif_riesgo_inherente_cc','nivel_riesgo_inherente_cc']]
    fig3 = px.scatter(df3_fig3, x="calif_impacto", y="calif_frecuencia", color="calif_riesgo_inherente_cc", size='calif_riesgo_inherente_cc', hover_data=['nivel_riesgo_inherente_cc'], color_continuous_scale='RdYlGn_r',
            labels={'calif_impacto':'Impacto', 'calif_frecuencia':'Frecuencia', 'calif_riesgo_inherente_cc':'Calificación'}, width=700, height= 500)
    fig3.update_layout(title_text="<b>Mapa de calor cualitativo<b>",title_x=0,margin= dict(l=0,r=10,b=10,t=30))
    st.write(fig3)
with col2:
    df7_fig7 = df1_matrizrop[['nivel_riesgo_inherente_cc','id_riesgo']]
    df7_fig7 = pd.DataFrame(df7_fig7.groupby(by=['nivel_riesgo_inherente_cc'], as_index=False).count())
    #st.write(df7_fig7)
    fig7 = px.bar(df7_fig7, x="nivel_riesgo_inherente_cc", y="id_riesgo", color = 'nivel_riesgo_inherente_cc',
                color_discrete_map={'MUY BAJO':'#79b36b','BAJO':'#adff99','MEDIO':'#ffff99','ALTO':'#ffce99','CRÍTICO':'#ff9999'},
                text_auto=True, width=700, height= 500,
                category_orders={"nivel_riesgo_inherente_cc": ['MUY BAJO','BAJO','MEDIO','ALTO','CRÍTICO']})
    fig7.update_layout(title_text="<b>Cantidad total de riesgos por nivel<b>",title_x=0,margin= dict(l=0,r=10,b=10,t=30),yaxis_title=None, xaxis_title=None,showlegend=False)
    st.write(fig7)

st.markdown("____")

df11_fig11 = df1_matrizrop[['nivel_riesgo_inherente_sc','factor_causal','tep_n1','tipo_efecto_inmediato']]

df11_fig11.insert(4, "nrsc", "")
df11_fig11.loc[df11_fig11.nivel_riesgo_inherente_sc=='CRÍTICO','nrsc'] = '5'
df11_fig11.loc[df11_fig11.nivel_riesgo_inherente_sc=='ALTO','nrsc'] = '4'
df11_fig11.loc[df11_fig11.nivel_riesgo_inherente_sc=='MEDIO','nrsc'] = '3'
df11_fig11.loc[df11_fig11.nivel_riesgo_inherente_sc=='BAJO','nrsc'] = '2'
df11_fig11.loc[df11_fig11.nivel_riesgo_inherente_sc=='MUY BAJO','nrsc'] = '1'
df11_fig11.nrsc = df11_fig11.nrsc.astype(int)

nivel_riesgo_inherente_sc_dim = go.parcats.Dimension(
                                                            values = df11_fig11.nivel_riesgo_inherente_sc,
                                                            label="Nivel de riesgo"
                                                            )  



factor_causal_dim = go.parcats.Dimension(
                                            values=df11_fig11.factor_causal,
                                            categoryorder='category ascending',
                                            label="Factor causal",
                                            
                                            )
    
tep_n1_dim = go.parcats.Dimension(
                                    values = df11_fig11.tep_n1,
                                    categoryorder='category ascending',
                                    label = "Tipo de evento"
                                    ) 

tipo_efecto_inmediato_dim = go.parcats.Dimension(
                                    values = df11_fig11.tipo_efecto_inmediato,
                                    categoryorder='category ascending',
                                    label = "Efecto inmediato"
                                    ) 

fig11 = go.Figure(data = [go.Parcats(dimensions=[nivel_riesgo_inherente_sc_dim, factor_causal_dim, tep_n1_dim],
                                    line={'color': df11_fig11.nrsc, 'colorscale':[[0, '#79b36b'],[0.25, '#adff99'],[0.5, '#ffff99'],[0.75, '#ffce99'], [1, 'rgb(255,0,0)']]},
                                    labelfont={'size': 15},
                                    tickfont={'size': 10})])
fig11.update_layout(title_text="<b>Mapa de relación:  factor causal - tipo de evento<b>",title_x=0.5,title_y=1,margin= dict(b=35,t=40),width=1300, height= 500)

st.write(fig11)
st.markdown('___')

fig12 = go.Figure(data = [go.Parcats(dimensions=[nivel_riesgo_inherente_sc_dim, factor_causal_dim],
                                    line={'color': df11_fig11.nrsc, 'colorscale':[[0, '#79b36b'],[0.25, '#adff99'],[0.5, '#ffff99'],[0.75, '#ffce99'], [1, 'rgb(255,0,0)']]},
                                    labelfont={'size': 15},
                                    tickfont={'size': 10})])
fig12.update_layout(title_text="<b>Mapa de relación:  factor causal - efecto inmediato<b>",title_x=0.5,title_y=1,margin= dict(b=35,t=40),width=1300, height= 500)

st.write(fig12)

st.markdown('___')

col1, col2, col3 = st.columns((0.3,3,1))
col1.write('')
df4_fig4 = df1_matrizrop[['fecha_identificacion','fecha','nivel_riesgo_inherente_cc','id_riesgo']]
df4_fig4 = df4_fig4.groupby(by=['fecha_identificacion','fecha','nivel_riesgo_inherente_cc'], as_index=False).count()
df4_fig4.set_index('fecha_identificacion', inplace=True)
#st.write(df4_fig4)
orden = ['ene./21',
'feb./21',
'mar./21',
'abr./21',
'may./21',
'jun./21',
'jul./21',
'ago./21',
'sep./21',
'oct./21',
'nov./21',
'dic./21',
]

df4_fig4 = df4_fig4.iloc[pd.Categorical(df4_fig4.index,orden).argsort()]

fig4 = px.bar(df4_fig4, x='fecha', y="id_riesgo",
            color='nivel_riesgo_inherente_cc', color_discrete_map={'MUY BAJO':'#79b36b','BAJO':'#adff99','MEDIO':'#ffff99','ALTO':'#ffce99','CRÍTICO':'#ff9999'}, barmode='group',
            width=1200, height= 490,
            category_orders={"fecha": [
                            'ene./20',
                            'feb./20',
                            'mar./20',
                            'abr./20',
                            'may./20',
                            'jun./20',
                            'jul./20',
                            'ago./20',
                            'sep./20',
                            'oct./20',
                            'nov./20',
                            'dic./20'
                            'ene./21',
                            'feb./21',
                            'mar./21',
                            'abr./21',
                            'may./21',
                            'jun./21',
                            'jul./21',
                            'ago./21',
                            'sep./21',
                            'oct./21',
                            'nov./21',
                            'dic./21'],
                            "nivel_riesgo_inherente_cc": ['MUY BAJO','BAJO','MEDIO','ALTO','CRÍTICO']},
             labels={'fecha':'Niveles de riesgo en cada mes', 'id_riesgo':'Cantidad de riesgos'})
fig4.update_layout(legend_title_text="Niveles de riesgo",title_text="<b>Evolución de la cantidad de riesgos por nivel<b>",title_x=0,margin= dict(l=0,r=10,b=10,t=30))
fig4.update_xaxes(rangeslider_visible=True)
col2.write(fig4)
col3.write('')
st.markdown("____")


### PARA CONTRUIR LAS ETIQUETAS DE RIESGO CUALITATIVO
df_datos1 = df1_matrizrop[['nivel_riesgo_inherente_cc','factor_causal','id_riesgo']]
df_datos1 = df_datos1.groupby(by=['nivel_riesgo_inherente_cc','factor_causal'], as_index=False).count()
#st.write(df_datos1)
cant_n5_fc = df_datos1.loc[df_datos1.loc[:,'nivel_riesgo_inherente_cc']=='CRÍTICO']
#st.write(cant_n5_fc)
df_datos2 = df1_matrizrop[['nivel_riesgo_inherente_cc','tep_n1','id_riesgo']]
df_datos2 = df_datos2.groupby(by=['nivel_riesgo_inherente_cc','tep_n1'], as_index=False).count()
#st.write(df_datos2)
cant_n5_tep = df_datos2.loc[df_datos2.loc[:,'nivel_riesgo_inherente_cc']=='CRÍTICO']
#st.write(cant_n5_tep)

cola, colb, coladic = st.columns((3,1,0.3))
with cola:
    ########  Cantidad de riesgos por nivel
    df5_fig5 = df1_matrizrop[['fecha','factor_causal','id_riesgo']]
    df5_fig5 = df5_fig5.groupby(by=['fecha','factor_causal'], as_index=False).count()
    #st.write(df5_fig5)
    fig5 = px.bar(df5_fig5, x="id_riesgo", y="fecha", orientation='h',
                color='factor_causal',color_discrete_map={'Eventos Externos':'#79b36b','Personas':'#adff99','Procesos':'#ffff99','TI':'#ffce99'},
                barmode='group',
                width = 900,
                height=430,
                category_orders={"fecha": [
                            'ene./20',
                            'feb./20',
                            'mar./20',
                            'abr./20',
                            'may./20',
                            'jun./20',
                            'jul./20',
                            'ago./20',
                            'sep./20',
                            'oct./20',
                            'nov./20',
                            'dic./20'
                            'ene./21',
                            'feb./21',
                            'mar./21',
                            'abr./21',
                            'may./21',
                            'jun./21',
                            'jul./21',
                            'ago./21',
                            'sep./21',
                            'oct./21',
                            'nov./21',
                            'dic./21']},
                labels={'fecha':'Factores causales en cada mes', 'id_riesgo':'Cantidad de riesgos'})
    fig5.update_layout(legend_title_text="Factor causal", title_text="<b>Cantidad de riesgos por factor causal - mensual<b>", title_x=0,margin= dict(l=0,r=10,b=10,t=30))
    st.write(fig5)


with colb:
    st.markdown("**Cantidad de riesgos CRÍTICO por factor causal:**")
    try:
        cant_n5_personas = cant_n5_fc.loc[cant_n5_fc.loc[:,'factor_causal']=='Personas']
        cant_n5_personas = cant_n5_personas.loc[:,'id_riesgo']
        colb.metric(label="CRÍTICO: FACTOR PERSONAS", value=str(int(cant_n5_personas)) +' riesgos')
    except (RuntimeError, TypeError, NameError):
        colb.metric(label="CRÍTICO: FACTOR PERSONAS", value='0')
    try:
        cant_n5_procesos = cant_n5_fc.loc[cant_n5_fc.loc[:,'factor_causal']=='Procesos']
        cant_n5_procesos = cant_n5_procesos.loc[:,'id_riesgo']
        colb.metric(label="CRÍTICO: FACTOR PROCESOS", value=str(int(cant_n5_procesos))+' riesgos')
    except (RuntimeError, TypeError, NameError):
        colb.metric(label="CRÍTICO: FACTOR PROCESOS", value='0')
    try:
        cant_n5_ti = cant_n5_fc.loc[cant_n5_fc.loc[:,'factor_causal']=='TI']
        cant_n5_ti = cant_n5_ti.loc[:,'id_riesgo']
        colb.metric(label="CRÍTICO: FACTOR T.I.", value=str(int(cant_n5_ti))+' riesgos', help = 'Tecnología de la Información')
    except (RuntimeError, TypeError, NameError):
        colb.metric(label="CRÍTICO: FACTOR T.I.", value='0', help = 'Tecnología de la Información')
    try:
        cant_n5_ee = cant_n5_fc.loc[cant_n5_fc.loc[:,'factor_causal']=='Eventos Externos']
        cant_n5_ee = cant_n5_ee.loc[:,'id_riesgo']
        colb.metric(label="CRÍTICO: FACTORES EXTERNOS", value=str(int(cant_n5_ee))+' riesgos', help = 'Eventos Externos')
    except (RuntimeError, TypeError, NameError):
        colb.metric(label="CRÍTICO: FACTORES EXTERNOS", value='0', help = 'Eventos Externos')

st.markdown("____")

coladic, cola, coladic2, colb = st.columns((0.3,1,0.15,3))
with cola:
    st.markdown("**Cantidad riesgos CRÍTICO por tipo de evento de pérdida:**")
    try:
        cant_n5_fe = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='1. Fraude Externo']
        cant_n5_fe = cant_n5_fe.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: FRAUDE EXTERNO", value=str(int(cant_n5_fe))+' riesgos')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: FRAUDE EXTERNO", value='0')
    try:
        cant_n5_fi = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='2. Fraude Interno']
        cant_n5_fi = cant_n5_fi.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: FRAUDE INTERNO", value=str(int(cant_n5_fi))+' riesgos')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: FRAUDE INTERNO", value='0')
    try:
        cant_n5_dp = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='3. Deficiencia en procesos']
        cant_n5_dp = cant_n5_dp.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: DEFICIENCIAS", value=str(int(cant_n5_dp))+' riesgos', help = 'Deficiencia en la ejecución de procesos, en el procesamiento de operaciones y en las relaciones con proveedores y terceros')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: DEFICIENCIAS", value='0', help = 'Deficiencia en la ejecución de procesos, en el procesamiento de operaciones y en las relaciones con proveedores y terceros')
    try:
        cant_n5_da = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='4. Daños de activos materiales']
        cant_n5_da = cant_n5_da.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: DAÑOS", value=str(int(cant_n5_da))+' riesgos', help = 'Daños de activos materiales')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: DAÑOS", value='0', help = 'Daños de activos materiales')
    try:
        cant_n5_in = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='5. Incidencias/fallos en T.I.']
        cant_n5_in = cant_n5_in.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: INCIDENCIAS", value=str(int(cant_n5_in))+' riesgos', help = 'Incidencias del negocio y fallos en los Sistemas de Información')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: INCIDENCIAS", value='0', help = 'Incidencias del negocio y fallos en los Sistemas de Información')
    try:
        cant_n5_pr = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='6. Prácticas con clientes/proveedores']
        cant_n5_pr = cant_n5_pr.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: PRÁCTICAS ADVERSAS", value=str(int(cant_n5_pr))+' riesgos', help = 'Prácticas con clientes, productos, proveedores y negocios')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: PRÁCTICAS ADVERSAS", value='0', help = 'Prácticas con clientes, productos, proveedores y negocios')
    try:
        cant_n5_re = cant_n5_tep.loc[cant_n5_tep.loc[:,'tep_n1']=='7. Relación/seguridad laboral']
        cant_n5_re = cant_n5_re.loc[:,'id_riesgo']
        cola.metric(label="CRÍTICO: LABORALES", value=str(int(cant_n5_re))+' riesgos', help = 'Relaciones laborales y seguridad en el puesto de trabajo')
    except (RuntimeError, TypeError, NameError):
        cola.metric(label="CRÍTICO: LABORALES", value='0', help = 'Relaciones laborales y seguridad en el puesto de trabajo')

with colb:
    ########  Cantidad de riesgos por nivel
    df8_fig8 = df1_matrizrop[['fecha','tep_n1','id_riesgo']]
    df8_fig8 = df8_fig8.groupby(by=['fecha','tep_n1'], as_index=False).count()
    #st.write(df5_fig5)
    fig8 = px.bar(df8_fig8, x="id_riesgo", y="fecha", orientation='h',
                color='tep_n1',color_discrete_map={'1. Fraude Externo':'#AF70FA',
                                                   '2. Fraude Interno':'#100BD4',
                                                   '3. Deficiencia en procesos':'#005AEB',
                                                   '4. Daños de activos materiales':'#0BAAD4',
                                                   '5. Incidencias/fallos en T.I.':'#16F5C4',
                                                   '6. Prácticas con clientes/proveedores':'#00EBB7',
                                                   '7. Relación/seguridad laboral':'#0BD44F'},
                barmode='group',
                width = 900,
                height=670,
                category_orders={"fecha": ['ene./21',
                                        'feb./21',
                                        'mar./21',
                                        'abr./21',
                                        'may./21',
                                        'jun./21',
                                        'jul./21',
                                        'ago./21',
                                        'sep./21',
                                        'oct./21',
                                        'nov./21',
                                        'dic./21'],
                                "tep_n1": ['1. Fraude Externo',
                                            '2. Fraude Interno',
                                            '3. Deficiencia en procesos',
                                            '4. Daños de activos materiales',
                                            '5. Incidencias/fallos en T.I.',
                                            '6. Prácticas con clientes/proveedores',
                                            '7. Relación/seguridad laboral']},
                labels={'fecha':'Tipo de evento en cada mes', 'id_riesgo':'Cantidad de riesgos','tep_n1':"" })
    fig8.update_xaxes(autorange='reversed')
    fig8.update_layout(legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=-0.1,
                        xanchor="right",
                        x=0.4),
                        title_text="<b>Cantidad de riesgos por tipo de evento - mensual<b>", title_x=0,margin= dict(l=0,r=10,b=10,t=30))
    
    st.write(fig8)

st.markdown("____")

col1, col2 = st.columns((1,1))
with col1:
    st.write("**Distribución de tipos de evento por nivel**")
    df6_fig6 = df1_matrizrop[['tep_n1','calif_riesgo_inherente_cc','nivel_riesgo_inherente_cc']]
    df6_fig6 = df6_fig6.groupby(by=['nivel_riesgo_inherente_cc','tep_n1'], as_index=False).count()
    #df6_fig6 = df6_fig6.style.applymap(nivel_riesgo_color, subset=['nivel_riesgo_inherente_cc'])
    #st.write(df6_fig6)
    df6_fig6_ = df6_fig6[['nivel_riesgo_inherente_cc', 'tep_n1']]
    df6_fig6_ = df6_fig6_.style.applymap(nivel_riesgo_color, subset=['nivel_riesgo_inherente_cc'])
    st.write(df6_fig6_)

with col2:
    df6a_fig6a = df1_matrizrop[['tep_n1']]
    df6a_fig6a['tep_n1_'] = df6a_fig6a['tep_n1']
    df6a_fig6a = df6a_fig6a.groupby(by=['tep_n1'], as_index=False).count()
    fig6a = px.pie(df6a_fig6a, values="tep_n1_", hole = 0.4 , names="tep_n1",
    category_orders={"tep_n1": ['1. Fraude Externo',
                                            '2. Fraude Interno',
                                            '3. Deficiencia en procesos',
                                            '4. Daños de activos materiales',
                                            '5. Incidencias/fallos en T.I.',
                                            '6. Prácticas con clientes/proveedores',
                                            '7. Relación/seguridad laboral']})
    fig6a.update_layout(legend_title_text="T.E. MUY BAJO", title_text="<b>Cantidad de riesgos por tipo de evento MUY BAJO<b>", title_x=0,margin= dict(l=0,r=10,b=10,t=30))
    st.write(fig6a)

st.markdown("___")
#col1,col2,col3 = st.columns((0.5,1,0.5))
#with col2:
#    st.write("**Mapa de distribución de tipos de evento por nivel**")
#    with st.expander('Mapa de distribución de tipos de evento por nivel'):
#        fig6 = px.sunburst(df6_fig6, path=['tep_n1', 'tep_n2', 'tep_n3'], values='calif_riesgo_inherente_cc', color='nivel_riesgo_inherente_cc',
#                            color_discrete_map={'MUY BAJO':'#79b36b','BAJO':'#adff99','MEDIO':'#ffff99','ALTO':'#ffce99','CRÍTICO':'#ff9999'},
#                            width=710, height= 650)
#        fig6.update_traces(hovertemplate='.')
#        fig6.update_layout(margin= dict(l=0,r=60,b=10,t=10))
#        st.write(fig6)
#st.markdown("___")
## COLUMNAS EN DATAFRAME df1_matrizrop
# fecha_identificacion
# id_riesgo
# descripcion_riesgo
# factor_causal
# efecto_inmediato_potencial_mayor
# tipo_efecto_inmediato
# tep_n3
# tep_n2
# tep_n1
# proceso
# macroproceso
# gerencia
# linea_negocio
# calif_impacto
# nivel_impacto
# calif_frecuencia
# nivel_frecuencia
# calif_riesgo_inherente_sc
# nivel_riesgo_inherente_sc
# calif_riesgo_inherente_cc
# nivel_riesgo_inherente_cc
# calif_riesgo_residual_enero
# nivel_riesgo_inherente_enero
# calif_riesgo_residual_febrero
# nivel_riesgo_inherente_febrero
# calif_riesgo_residual_marzo
# nivel_riesgo_inherente_marzo


col1, col2 = st.columns((0.8,1))
with col1:
    st.write("**Cantidad de riesgos por gerencia y nivel de riesgo**")
    df10 = df1_matrizrop[['nivel_riesgo_inherente_cc','gerencia']]
    df10['cantidad_riesgos'] = df10['gerencia']
    df10 = df10.groupby(by=['nivel_riesgo_inherente_cc','gerencia'], as_index=False).count()
    df10 = df10.style.applymap(nivel_riesgo_color, subset=['nivel_riesgo_inherente_cc'])
    col1.write(df10)
with col2:
    st.write("**Cantidad de riesgos por proceso y nivel de riesgo**")
    df9 = df1_matrizrop[['nivel_riesgo_inherente_cc','proceso']]
    df9['cantidad_riesgos'] = df9['proceso']
    df9 = df9.groupby(by=['nivel_riesgo_inherente_cc','proceso'], as_index=False).count()
    df9 = df9.style.applymap(nivel_riesgo_color, subset=['nivel_riesgo_inherente_cc'])
    col2.write(df9)

st.markdown("___")
col1, col2, col3 = st.columns((0.1,1,0.2))
with col2:
    df13_fig13 = df1_matrizrop[['nivel_riesgo_inherente_sc','factor_causal','tep_n1','id_riesgo']]
    df13_fig13 = df13_fig13.groupby(by=['nivel_riesgo_inherente_sc','factor_causal','tep_n1'], as_index=False).count()
    fig13 = px.treemap(df13_fig13, path=[px.Constant("all"), 'nivel_riesgo_inherente_sc', 'factor_causal','tep_n1'], values='id_riesgo', color='nivel_riesgo_inherente_sc',
                        color_discrete_map={'MUY BAJO':'#79b36b','BAJO':'#adff99','MEDIO':'#ffff99','ALTO':'#ffce99','CRÍTICO':'#ff9999'}, width=1200, height=600)
    fig13.update_traces(root_color="lightgrey")
    fig13.update_layout(title_text="<b>Agrupación por nivel y proceso<b>", title_x=0.5,title_y=1,margin= dict(b=35,t=40))
    st.write(fig13)
