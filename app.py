"""
============================================================
TFM - HERRAMIENTA DE DIRECCIÓN DEPORTIVA Y SCOUTING
Atlético de Madrid | Temporada 26/27
Master Big Data y Análisis de Datos en el Deporte
Diego Alejandro Espinoza Gonzalez
============================================================
Ejecutar: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Atlético de Madrid | Dirección Deportiva 26/27",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Colores corporativos Atlético de Madrid
ROJO  = "#CC2020"
AZUL  = "#1B2870"
BLANC = "#FFFFFF"
GRIS  = "#F5F5F5"

# CSS personalizado
st.markdown(f"""
<style>
    .main {{ background-color: #FAFAFA; }}
    .sidebar .sidebar-content {{ background-color: {AZUL}; }}
    .metric-card {{
        background: white; border-left: 4px solid {ROJO};
        padding: 1rem; border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }}
    .titulo-seccion {{
        color: {AZUL}; font-size: 1.8rem;
        font-weight: 700; border-bottom: 3px solid {ROJO};
        padding-bottom: 0.5rem; margin-bottom: 1.5rem;
    }}
    .jugador-card {{
        background: white; border: 1px solid #ddd;
        border-top: 4px solid {ROJO}; border-radius: 8px;
        padding: 1.2rem; margin-bottom: 1rem;
    }}
    .badge {{
        display: inline-block; padding: 3px 10px;
        border-radius: 12px; font-size: 0.8rem;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CARGA DE DATOS (cacheada)
# ─────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    try:
        jugadores   = pd.read_csv("master_jugadores.csv",    encoding="utf-8-sig")
        cinco_ligas = pd.read_csv("master_5_ligas.csv",      encoding="utf-8-sig")
        modelo      = pd.read_csv("modelo_juego_laliga.csv", encoding="utf-8-sig")
        candidatos  = pd.read_csv("scouting_candidatos.csv", encoding="utf-8-sig")
        fichajes    = pd.read_csv("fichajes_objetivo.csv",   encoding="utf-8-sig")
        plantilla   = pd.read_csv("plantilla_salarios.csv",  encoding="utf-8-sig")
        financiero  = pd.read_csv("fichajes_financiero.csv", encoding="utf-8-sig")
        return jugadores, cinco_ligas, modelo, candidatos, fichajes, plantilla, financiero
    except FileNotFoundError as e:
        st.error(f"Archivo no encontrado: {e}. Asegúrate de que todos los CSV están en la misma carpeta que app.py")
        st.stop()

jugadores, cinco_ligas, modelo, candidatos, fichajes, plantilla, financiero = cargar_datos()


# ─────────────────────────────────────────────
# IMÁGENES: escudo y fondo del estadio
# ─────────────────────────────────────────────
def img_base64(ruta):
    """Lee una imagen local y la devuelve en base64, o None si no existe."""
    if os.path.exists(ruta):
        with open(ruta, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Fondo: estadio Riyadh Air Metropolitano (archivo estadio.jpg en la carpeta)
fondo = img_base64("estadio.jpg")
if fondo:
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(10,12,25,0.72), rgba(10,12,25,0.80)),
                          url("data:image/jpg;base64,{fondo}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    /* Texto blanco nitido en el area principal */
    section.main p, section.main li, section.main span,
    section.main h1, section.main h2, section.main h3,
    section.main label, section.main [data-testid="stMarkdownContainer"] {{
        color: #FFFFFF !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.6);
    }}
    /* Titulos de seccion en blanco */
    .titulo-seccion {{ color: #FFFFFF !important; }}
    /* Tarjetas de metricas con fondo oscuro translucido y texto blanco */
    div[data-testid="stMetric"] {{
        background: rgba(20,24,45,0.75);
        padding: 0.8rem 1rem; border-radius: 8px;
        border-left: 4px solid {ROJO};
    }}
    div[data-testid="stMetric"] * {{ color: #FFFFFF !important; }}
    /* Tablas y dataframes legibles */
    section.main [data-testid="stDataFrame"] {{ background: rgba(255,255,255,0.96); border-radius: 8px; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR NAVEGACIÓN
# ─────────────────────────────────────────────
with st.sidebar:
    escudo = img_base64("escudo.png")
    if escudo:
        st.markdown(f"""
        <div style='text-align:center; padding:1rem 0;'>
            <img src="data:image/png;base64,{escudo}" width="110"><br>
            <div style='color:{ROJO}; font-size:1.3rem; font-weight:700; margin-top:0.5rem;'>ATLÉTICO DE MADRID</div>
            <div style='color:#888; font-size:0.85rem;'>Dirección Deportiva 26/27</div>
        </div>
        <hr style='border-color:#ffffff33;'>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='text-align:center; padding:1rem 0;'>
            <div style='font-size:2.5rem;'>⚽</div>
            <div style='color:{ROJO}; font-size:1.3rem; font-weight:700;'>ATLÉTICO DE MADRID</div>
            <div style='color:#888; font-size:0.85rem;'>Dirección Deportiva 26/27</div>
        </div>
        <hr style='border-color:#ffffff33;'>
        """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación",
        ["🏟️ Modelo de Juego",
         "👥 Plantilla",
         "👤 Análisis Individual",
         "🔍 Scouting",
         "⚖️ Comparador",
         "🎯 Fichajes Objetivo",
         "💶 Análisis Financiero"],
        label_visibility="collapsed"
    )
    st.markdown("<hr style='border-color:#ffffff33;'>", unsafe_allow_html=True)
    st.caption("Master Big Data y Análisis de Datos\nEscuela Universitaria Real Madrid")


# ══════════════════════════════════════════════
# PÁGINA 1: MODELO DE JUEGO
# ══════════════════════════════════════════════
if pagina == "🏟️ Modelo de Juego":
    st.markdown('<div class="titulo-seccion">🏟️ Modelo de Juego — Atlético de Madrid 25/26</div>', unsafe_allow_html=True)

    atleti = modelo[modelo["es_atleti"] == True].iloc[0]
    pj = int(atleti["total games"])

    # KPIs resumen (4 tarjetas)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Goles por partido", f"{atleti['Goles_pp']:.2f}", delta="Rank 4/20")
    with col2:
        st.metric("% Acierto de pase", f"{atleti['Posesion_proxy_pct']:.0f}%", delta="Rank 3/20")
    with col3:
        st.metric("Goles encajados/p", f"{atleti['Goles_encajados_pp']:.2f}", delta="Rank 3/20")
    with col4:
        st.metric("Porterías a cero %", f"{atleti['Porteria_cero_pct']:.0f}%", delta="Rank 1/20 🏆")

    st.markdown("---")

    # Radar de percentiles
    col_radar, col_texto = st.columns([3, 2])
    with col_radar:
        kpis_radar = {
            "Goles": "Goles_pp_pct",
            "Tiros": "Tiros_pp_pct",
            "Tiros a puerta": "Tiros_puerta_pp_pct",
            "Conversión": "Conversion_pct_pct",
            "Posesión": "Posesion_proxy_pct_pct",
            "Pases": "Pases_pp_pct",
            "Toques área": "Toques_area_riv_pp_pct",
            "Centros": "Centros_pp_pct",
            "Goles encaj.": "Goles_encajados_pp_pct",
            "Tiros concedidos": "Tiros_concedidos_pp_pct",
            "Tiros conc. área": "Tiros_conc_area_pp_pct",
            "Portería a cero": "Porteria_cero_pct_pct",
            "Entradas gan.": "Entradas_ganadas_pct_pct",
            "Duelos gan.": "Duelos_ganados_pct_pct",
        }
        etiquetas = list(kpis_radar.keys())
        valores_atleti = [float(atleti.get(v, 50)) for v in kpis_radar.values()]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=valores_atleti + [valores_atleti[0]],
            theta=etiquetas + [etiquetas[0]],
            fill="toself",
            name="Atlético de Madrid",
            line=dict(color=ROJO, width=2),
            fillcolor=f"rgba(204,32,32,0.25)"
        ))
        fig.add_trace(go.Scatterpolar(
            r=[50]*len(etiquetas) + [50],
            theta=etiquetas + [etiquetas[0]],
            name="Media La Liga",
            line=dict(color=AZUL, width=1.5, dash="dash"),
            fillcolor="rgba(0,0,0,0)"
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title=dict(text=f"Perfil de Juego — Percentiles La Liga ({pj} partidos)", x=0.5),
            height=450,
            margin=dict(t=60, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_texto:
        st.markdown(f"""
        ### Clasificación del Estilo
        <div style='background:{ROJO}; color:white; padding:0.8rem; border-radius:8px; text-align:center; font-size:1.2rem; font-weight:700;'>
        DOMINANTE CON BASE DEFENSIVA DE ÉLITE
        </div>
        <br>
        """, unsafe_allow_html=True)

        fases = {
            "⚔️ Ataque / Posesión": [("Posesión (% pase)", f"{atleti['Posesion_proxy_pct']:.0f}%", "3/20"),
                                     ("Pases / partido", f"{atleti['Pases_pp']:.0f}", "3/20"),
                                     ("Toques área rival", f"{atleti['Toques_area_riv_pp']:.1f}", "3/20")],
            "🎯 Finalización":      [("Goles / partido", f"{atleti['Goles_pp']:.2f}", "4/20"),
                                     ("Tiros a puerta", f"{atleti['Tiros_puerta_pp']:.2f}", "3/20"),
                                     ("% Conversión", f"{atleti['Conversion_pct']:.0f}%", "7/20")],
            "🛡️ Defensa":           [("Goles encajados", f"{atleti['Goles_encajados_pp']:.2f}", "3/20"),
                                     ("Portería a cero", f"{atleti['Porteria_cero_pct']:.0f}%", "1/20 🏆"),
                                     ("Tiros conc. área", f"{atleti['Tiros_conc_area_pp']:.2f}", "3/20")],
        }
        for fase, stats in fases.items():
            st.markdown(f"**{fase}**")
            for nombre, valor, rank in stats:
                st.markdown(f"&nbsp;&nbsp;• {nombre}: **{valor}** *(rank {rank})*")

    # Resumen del estilo + alineación tipo
    st.markdown("---")
    st.subheader("📝 Resumen del Estilo de Juego")
    col_res, col_xi = st.columns([3, 2])
    with col_res:
        st.markdown(f"""
        El Atlético de Madrid 25/26 ha evolucionado hacia un **equipo dominante de posesión**,
        rompiendo con el cliché reactivo. Es **top-3 de La Liga** en control de balón
        (86% de acierto de pase, 518 pases por partido) y en juego en campo rival
        (29 toques en el área contraria por encuentro), llevando siempre la iniciativa.

        Mantiene su **ADN defensivo de élite**: es el equipo con **más porterías a cero de la liga**
        (40% de los partidos) y de los que menos remates concede dentro del área.

        El punto de mejora está en la **finalización**: pese a generar mucho (4º en goles,
        3º en tiros a puerta), solo es 7º en conversión. Genera ocasiones de sobra, pero
        necesita más eficiencia en el último pase y el remate.

        **En resumen:** un bloque que domina con balón, ataca de forma posicional y
        defiende con solidez, basado en un **4-4-2** compacto que se estira en ataque.
        """)
    with col_xi:
        st.markdown(f"""
        <div style='background:rgba(27,40,112,0.06); border-radius:10px; padding:1rem; text-align:center;'>
        <div style='color:{AZUL}; font-weight:700; font-size:1.1rem; margin-bottom:0.8rem;'>ALINEACIÓN TIPO (4-4-2)</div>
        <div style='margin:0.6rem 0;'><span style='background:{ROJO}; color:white; padding:4px 14px; border-radius:14px;'>⚪ Oblak</span></div>
        <div style='margin:0.6rem 0; font-size:0.92rem;'>
            <span style='background:{AZUL}; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Molina</span>
            <span style='background:{AZUL}; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Le Normand</span>
            <span style='background:{AZUL}; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Hancko</span>
            <span style='background:{AZUL}; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Ruggeri</span>
        </div>
        <div style='margin:0.6rem 0; font-size:0.92rem;'>
            <span style='background:#1a7a4a; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Llorente</span>
            <span style='background:#1a7a4a; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Barrios</span>
            <span style='background:#1a7a4a; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Koke</span>
            <span style='background:#1a7a4a; color:white; padding:3px 10px; border-radius:12px; margin:2px;'>Baena</span>
        </div>
        <div style='margin:0.6rem 0;'>
            <span style='background:#e07000; color:white; padding:4px 12px; border-radius:14px; margin:2px;'>J. Álvarez</span>
            <span style='background:#e07000; color:white; padding:4px 12px; border-radius:14px; margin:2px;'>Sørloth</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

    # Comparativa liga
    st.markdown("---")
    st.subheader("📊 Comparativa con los 20 equipos de La Liga")
    metrica_sel = st.selectbox(
        "Selecciona una métrica:",
        ["Goles_pp","Posesion_proxy_pct","Pases_pp","Tiros_pp",
         "Goles_encajados_pp","Porteria_cero_pct","Tiros_concedidos_pp","Conversion_pct"],
        format_func=lambda x: x.replace("_pp","").replace("_pct","").replace("_"," ").title()
    )
    modelo_sorted = modelo.sort_values(metrica_sel, ascending=False)
    colores_bar = [ROJO if e else AZUL for e in modelo_sorted["es_atleti"]]
    fig2 = px.bar(
        modelo_sorted, x="equipo", y=metrica_sel,
        color_discrete_sequence=[AZUL],
        labels={"equipo": "Equipo", metrica_sel: metrica_sel.replace("_"," ")},
        height=350
    )
    fig2.update_traces(marker_color=colores_bar)
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════
# PÁGINA 2: PLANTILLA
# ══════════════════════════════════════════════
elif pagina == "👥 Plantilla":
    st.markdown('<div class="titulo-seccion">👥 Plantilla — Atlético de Madrid 25/26</div>', unsafe_allow_html=True)

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pos_filtro = st.multiselect("Filtrar por posición:", ["Goalkeeper","Defender","Midfielder","Forward"],
                                    default=["Goalkeeper","Defender","Midfielder","Forward"])
    with col_f2:
        min_min = st.slider("Minutos mínimos:", 0, 2500, 450, 100)

    df_plantilla = jugadores[
        (jugadores["posicion"].isin(pos_filtro)) &
        (jugadores["Time Played"] >= min_min)
    ].copy()

    # Traducir posición
    trad = {"Goalkeeper":"Portero","Defender":"Defensa","Midfielder":"Centrocampista","Forward":"Delantero"}
    df_plantilla["Posición"] = df_plantilla["posicion"].map(trad)

    st.markdown(f"**{len(df_plantilla)} jugadores** con ≥{min_min} minutos")

    # Tabla interactiva
    cols_tabla = ["nombre","Posición","Time Played","Goals p90","Total Passes p90",
                  "Pass Accuracy %","Duel Win %","Shots on Target %","Save Ratio %"]
    cols_ok = [c for c in cols_tabla if c in df_plantilla.columns]
    df_show = df_plantilla[cols_ok].rename(columns={
        "nombre":"Jugador","Time Played":"Minutos","Goals p90":"Goles/90",
        "Total Passes p90":"Pases/90","Pass Accuracy %":"% Pase",
        "Duel Win %":"% Duelos","Shots on Target %":"% Tiros Puerta","Save Ratio %":"% Paradas"
    }).sort_values("Minutos", ascending=False)

    st.dataframe(
        df_show.style.format({
            "Minutos":"{:.0f}","Goles/90":"{:.2f}","Pases/90":"{:.1f}",
            "% Pase":"{:.1f}","% Duelos":"{:.1f}","% Tiros Puerta":"{:.1f}","% Paradas":"{:.1f}"
        }).background_gradient(subset=["Minutos"], cmap="Reds"),
        use_container_width=True, height=400
    )

    # Gráfico comparativo
    st.markdown("---")
    st.subheader("📊 Comparativa visual de jugadores")
    col_x, col_y = st.columns(2)
    metricas_disp = ["Goals p90","Total Passes p90","Pass Accuracy %","Duel Win %",
                     "Aerial Win %","Tackle Win %","Interceptions p90",
                     "Shots on Target %","Key Passes (Attempt Assists) p90"]
    metricas_ok = [m for m in metricas_disp if m in df_plantilla.columns]
    with col_x:
        eje_x = st.selectbox("Eje X:", metricas_ok, index=0)
    with col_y:
        eje_y = st.selectbox("Eje Y:", metricas_ok, index=1 if len(metricas_ok)>1 else 0)

    fig3 = px.scatter(
        df_plantilla, x=eje_x, y=eje_y, text="nombre", color="Posición",
        color_discrete_map={"Portero":AZUL,"Defensa":"#1a7a4a","Centrocampista":ROJO,"Delantero":"#e07000"},
        labels={eje_x: eje_x.replace("_"," "), eje_y: eje_y.replace("_"," ")},
        height=450
    )
    fig3.update_traces(textposition="top center", marker=dict(size=10))
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════
# PÁGINA 3: SCOUTING
# ══════════════════════════════════════════════
elif pagina == "🔍 Scouting":
    st.markdown('<div class="titulo-seccion">🔍 Motor de Scouting — 5 Grandes Ligas</div>', unsafe_allow_html=True)

    st.info(f"📊 Base de datos: **{len(cinco_ligas):,} jugadores** en 5 ligas | "
            f"**{cinco_ligas[cinco_ligas['muestra_fiable']==True].shape[0]}** con muestra fiable (≥450 min)")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        pos_sel = st.selectbox("Posición:", ["Todas","Forward","Midfielder","Defender","Goalkeeper"])
    with col2:
        ligas_disp = sorted(cinco_ligas["liga"].dropna().unique().tolist())
        ligas_sel = st.multiselect("Ligas:", ligas_disp, default=ligas_disp)
    with col3:
        solo_fiable = st.checkbox("Solo muestra fiable (≥450 min)", value=True)

    df_scout = cinco_ligas.copy()
    if pos_sel != "Todas":
        df_scout = df_scout[df_scout["posicion"] == pos_sel]
    if ligas_sel:
        df_scout = df_scout[df_scout["liga"].isin(ligas_sel)]
    if solo_fiable:
        df_scout = df_scout[df_scout["muestra_fiable"] == True]

    st.markdown(f"**{len(df_scout)} jugadores** encontrados")

    # Comparador: dos métricas
    st.markdown("---")
    st.subheader("📊 Comparador de métricas")
    metricas_scout = [c for c in ["Goals p90","Total Passes p90","Pass Accuracy %",
                                   "Duel Win %","Aerial Win %","Tackle Win %","Interceptions p90",
                                   "Shots on Target %","Key Passes (Attempt Assists) p90",
                                   "Save Ratio %","Progressive Carries p90"]
                      if c in df_scout.columns]
    col_a, col_b = st.columns(2)
    with col_a:
        met_x = st.selectbox("Métrica X:", metricas_scout, key="sx")
    with col_b:
        met_y = st.selectbox("Métrica Y:", metricas_scout, index=1 if len(metricas_scout)>1 else 0, key="sy")

    df_scout["es_atleti_label"] = df_scout["equipo"].apply(
        lambda x: "Atlético de Madrid" if x == "Club Atlético de Madrid" else x
    )
    df_scout["color_label"] = df_scout["equipo"].apply(
        lambda x: "Atlético" if x == "Club Atlético de Madrid" else df_scout.loc[df_scout["equipo"]==x,"liga"].values[0] if len(df_scout.loc[df_scout["equipo"]==x]) > 0 else "Otro"
    )
    fig4 = px.scatter(
        df_scout, x=met_x, y=met_y,
        hover_data=["nombre","equipo","liga","Time Played"],
        color="liga",
        labels={met_x: met_x, met_y: met_y},
        height=450
    )
    # Resaltar Atleti
    df_atleti_scout = df_scout[df_scout["equipo"]=="Club Atlético de Madrid"]
    if not df_atleti_scout.empty:
        fig4.add_trace(go.Scatter(
            x=df_atleti_scout[met_x], y=df_atleti_scout[met_y],
            mode="markers+text", text=df_atleti_scout["nombre"],
            textposition="top center",
            marker=dict(color=ROJO, size=14, symbol="star", line=dict(width=1, color="white")),
            name="Atlético de Madrid"
        ))
    st.plotly_chart(fig4, use_container_width=True)

    # Tabla top jugadores
    st.markdown("---")
    st.subheader("🏆 Top candidatos por similitud con el Atleti")
    trad = {"Goalkeeper":"Portero","Defender":"Defensa","Midfielder":"Centrocampista","Forward":"Delantero"}
    candidatos["Posición"] = candidatos["posicion"].map(trad).fillna(candidatos["posicion"])

    for pos in ["Forward","Midfielder","Defender","Goalkeeper"]:
        sub = candidatos[candidatos["posicion"]==pos].sort_values("similitud",ascending=False).head(5)
        if sub.empty: continue
        with st.expander(f"🏷️ {trad.get(pos, pos)} — Top 5 similares al Atleti"):
            cols_cand = ["nombre","equipo","liga","similitud","Time Played"]
            extra = {"Forward":["Goals p90","Shots on Target %"],
                     "Midfielder":["Total Passes p90","Pass Accuracy %"],
                     "Defender":["Duel Win %","Aerial Win %"],
                     "Goalkeeper":["Save Ratio %"]}
            for c in extra.get(pos, []):
                if c in sub.columns: cols_cand.append(c)
            st.dataframe(sub[[c for c in cols_cand if c in sub.columns]].rename(
                columns={"nombre":"Jugador","equipo":"Club","liga":"Liga",
                         "similitud":"Similitud %","Time Played":"Minutos"}
            ), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PÁGINA 2.5: ANÁLISIS INDIVIDUAL
# ══════════════════════════════════════════════
elif pagina == "👤 Análisis Individual":
    st.markdown('<div class="titulo-seccion">👤 Análisis Individual — Perfil completo del jugador</div>', unsafe_allow_html=True)
    st.markdown("Explora el rendimiento de cualquier jugador con su radar de percentiles, estadísticas clave y "
                "perfil de fortalezas y debilidades frente a su posición en las **5 grandes ligas**.")

    POS_MAP = {"Delantero": "Forward", "Centrocampista": "Midfielder",
               "Defensa": "Defender", "Portero": "Goalkeeper"}
    POS_ES = {v: k for k, v in POS_MAP.items()}
    LIGA_ES = {"Italy_Serie_A": "Serie A 🇮🇹", "Spain_Primera_Division": "LaLiga 🇪🇸",
               "England_Premier_League": "Premier League 🏴", "Germany_Bundesliga": "Bundesliga 🇩🇪",
               "France_Ligue_1": "Ligue 1 🇫🇷"}

    # Perfil de KPIs por posición: (columna, etiqueta_radar, frase_fortaleza, frase_debilidad, invertir)
    PERFIL = {
        "Forward": [
            ("Goals p90", "Goles", "Mucho gol", "Poco gol", False),
            ("Total Big Chances Scored p90", "Grandes ocasiones", "Define grandes ocasiones", "Falla grandes ocasiones", False),
            ("Shots On Target ( inc goals ) p90", "Tiros a puerta", "Gran puntería", "Poca puntería", False),
            ("Total Shots p90", "Tiros", "Dispara mucho", "Dispara poco", False),
            ("Total Touches In Opposition Box p90", "Toques área", "Vive en el área", "Poca presencia en área", False),
            ("Successful Dribbles p90", "Regates", "Buen regate", "Regate flojo", False),
            ("Key Passes (Attempt Assists) p90", "Pases clave", "Genera juego", "Genera poco juego", False),
            ("Goal Assists p90", "Asistencias", "Asiste bien", "Asiste poco", False),
            ("Aerial Duels won p90", "Aéreos gan.", "Fuerte de cabeza", "Débil de cabeza", False),
            ("Total Losses Of Possession p90", "Cuida balón", "Cuida el balón", "Pierde muchos balones", True),
        ],
        "Midfielder": [
            ("Total Passes p90", "Pases", "Mucho volumen de pase", "Poco volumen de pase", False),
            ("Pass Accuracy %", "% Pase", "Pase muy preciso", "Pase impreciso", False),
            ("Key Passes (Attempt Assists) p90", "Pases clave", "Crea ocasiones", "Crea pocas ocasiones", False),
            ("Shots Created p90", "Ocasiones creadas", "Genera mucho", "Genera poco", False),
            ("Successful Dribbles p90", "Regates", "Bueno al regate", "Regate flojo", False),
            ("Progressive Carries p90", "Conducciones", "Progresa con balón", "Progresa poco", False),
            ("Forward Passes p90", "Pases adelante", "Pase vertical", "Pase poco vertical", False),
            ("Interceptions p90", "Intercepciones", "Buen anticipo", "Poco anticipo", False),
            ("Tackles Won p90", "Entradas gan.", "Roba bien", "Roba poco", False),
            ("Recoveries p90", "Recuperaciones", "Recupera mucho", "Recupera poco", False),
        ],
        "Defender": [
            ("Total Clearances p90", "Despejes", "Despeja mucho", "Despeja poco", False),
            ("Interceptions p90", "Intercepciones", "Gran anticipo", "Poco anticipo", False),
            ("Total Tackles p90", "Entradas", "Entra mucho", "Entra poco", False),
            ("Tackles Won p90", "Entradas gan.", "Entra con éxito", "Falla entradas", False),
            ("Aerial Duels won p90", "Aéreos gan.", "Dominante por alto", "Flojo por alto", False),
            ("Aerial Win %", "% Aéreos", "Gana casi todos los aéreos", "Pierde muchos aéreos", False),
            ("Blocks p90", "Bloqueos", "Bloquea mucho", "Bloquea poco", False),
            ("Recoveries p90", "Recuperaciones", "Recupera mucho", "Recupera poco", False),
            ("Duel Win %", "% Duelos", "Gana duelos", "Pierde duelos", False),
            ("Pass Accuracy %", "% Pase", "Saca el balón limpio", "Impreciso con balón", False),
        ],
        "Goalkeeper": [
            ("Saves Made p90", "Paradas", "Para mucho", "Para poco", False),
            ("Save Ratio %", "% Paradas", "Gran ratio de paradas", "Ratio de paradas bajo", False),
            ("Saves Made from Inside Box p90", "Paradas área", "Salva en el área", "Flojo en el área", False),
            ("Saves Made from Outside Box p90", "Paradas lejos", "Para de lejos", "Flojo en disparos lejanos", False),
            ("Penalties Saved p90", "Penaltis", "Para penaltis", "No para penaltis", False),
            ("Catches p90", "Blocadas", "Seguro en blocaje", "Inseguro en blocaje", False),
            ("Punches p90", "Despejes puño", "Despeja con puños", "Pocos despejes de puño", False),
            ("GK Successful Distribution p90", "Distribución", "Buena distribución", "Distribución pobre", False),
            ("Pass Accuracy %", "% Pase", "Bueno con los pies", "Flojo con los pies", False),
            ("Goals Conceded p90", "Goles encaj.", "Encaja poco", "Encaja mucho", True),
        ],
    }

    # ── Buscador de jugador ──
    cf1, cf2, cf3 = st.columns([1, 1, 2])
    with cf1:
        pos_filtro = st.selectbox("Posición:", ["Todas"] + list(POS_MAP.keys()))
    with cf2:
        ligas_disp = sorted(cinco_ligas["liga"].dropna().unique().tolist())
        liga_filtro = st.selectbox("Liga:", ["Todas"] + [LIGA_ES.get(l, l) for l in ligas_disp])
    base = cinco_ligas[cinco_ligas["muestra_fiable"] == True].copy()
    if pos_filtro != "Todas":
        base = base[base["posicion"] == POS_MAP[pos_filtro]]
    if liga_filtro != "Todas":
        liga_key = [k for k, v in LIGA_ES.items() if v == liga_filtro]
        if liga_key:
            base = base[base["liga"] == liga_key[0]]
    base = base.reset_index(drop=True)

    # Etiquetas únicas
    etqs, mapa, vistos = [], {}, {}
    for i, r in base.iterrows():
        eq = "Atlético de Madrid" if r["equipo"] == "Club Atlético de Madrid" else r["equipo"]
        lab = f"{r['nombre']} · {eq}"
        if lab in vistos:
            lab = f"{lab} ({i})"
        vistos[lab] = i; mapa[lab] = i
        etqs.append(lab)
    with cf3:
        jugador_sel = st.selectbox("🔍 Busca un jugador:", etqs,
                                   index=0 if etqs else None,
                                   help="Filtra por posición/liga y escribe el nombre")

    if not jugador_sel:
        st.info("No hay jugadores con los filtros seleccionados.")
    else:
        row = base.loc[mapa[jugador_sel]]
        pos_en = row["posicion"]
        kpis = PERFIL[pos_en]

        # Pool de su posición (fiable) para percentiles
        pool = cinco_ligas[(cinco_ligas["posicion"] == pos_en) &
                           (cinco_ligas["muestra_fiable"] == True)].copy()

        def pctl(col, val, inv=False):
            s = pool[col].dropna()
            if len(s) == 0:
                return 50.0
            p = (s < val).mean() * 100
            return round(100 - p, 0) if inv else round(p, 0)

        # Percentiles de todas las métricas del perfil
        pcts = [pctl(c, row.get(c, 0) or 0, inv) for c, _, _, _, inv in kpis]
        etiquetas_kpi = [lab for _, lab, _, _, _ in kpis]

        eq_nombre = "Atlético de Madrid" if row["equipo"] == "Club Atlético de Madrid" else row["equipo"]

        # ───────── LAYOUT: ficha (izq) + radar (der) ─────────
        col_ficha, col_radar = st.columns([2, 3])

        with col_ficha:
            es_atleti = row["equipo"] == "Club Atlético de Madrid"
            borde = ROJO if es_atleti else AZUL
            st.markdown(f"""
            <div style='background:rgba(20,24,45,0.85); border-top:5px solid {borde};
                        border-radius:10px; padding:1.2rem; text-align:center;'>
                <div style='font-size:1.6rem; font-weight:800; color:#fff;'>{row['nombre']}</div>
                <div style='color:{ROJO}; font-weight:700; margin:0.3rem 0;'>{POS_ES.get(pos_en, pos_en)}
                    {'· #'+str(int(row['dorsal'])) if pd.notna(row.get('dorsal')) else ''}</div>
                <div style='color:#bbb; font-size:0.95rem;'>{eq_nombre}</div>
                <div style='color:#888; font-size:0.85rem;'>{LIGA_ES.get(row['liga'], row['liga'])}</div>
            </div>
            """, unsafe_allow_html=True)

            # Mapa de posición (campo vertical realista con punto)
            zona_v = {"Goalkeeper": 90, "Defender": 70, "Midfielder": 48, "Forward": 22}.get(pos_en, 50)
            dorsal_txt = str(int(row['dorsal'])) if pd.notna(row.get('dorsal')) else ""
            bl = "rgba(255,255,255,0.55)"  # líneas
            st.markdown(f"""
            <div style='margin-top:0.8rem; text-align:center; color:#ccc; font-weight:600;'>Zona de juego</div>
            <div style='position:relative; width:175px; height:250px; margin:0.4rem auto 0;
                        border:2px solid {bl}; border-radius:6px;
                        background:repeating-linear-gradient(0deg,#1f7a44 0 25px,#1b6e3c 25px 50px);'>
                <!-- línea de medio campo -->
                <div style='position:absolute; left:0; right:0; top:50%; height:2px; background:{bl};'></div>
                <!-- círculo central -->
                <div style='position:absolute; left:50%; top:50%; width:48px; height:48px;
                            transform:translate(-50%,-50%); border:2px solid {bl}; border-radius:50%;'></div>
                <!-- área superior (portería rival) -->
                <div style='position:absolute; left:50%; top:0; width:80px; height:38px;
                            transform:translateX(-50%); border:2px solid {bl}; border-top:none;'></div>
                <div style='position:absolute; left:50%; top:0; width:40px; height:16px;
                            transform:translateX(-50%); border:2px solid {bl}; border-top:none;'></div>
                <!-- área inferior (portería propia) -->
                <div style='position:absolute; left:50%; bottom:0; width:80px; height:38px;
                            transform:translateX(-50%); border:2px solid {bl}; border-bottom:none;'></div>
                <div style='position:absolute; left:50%; bottom:0; width:40px; height:16px;
                            transform:translateX(-50%); border:2px solid {bl}; border-bottom:none;'></div>
                <!-- jugador -->
                <div style='position:absolute; left:50%; top:{zona_v}%; transform:translate(-50%,-50%);
                            width:34px; height:34px; background:{ROJO}; border:3px solid #fff;
                            border-radius:50%; box-shadow:0 2px 8px rgba(0,0,0,0.6);
                            display:flex; align-items:center; justify-content:center;
                            color:#fff; font-weight:800; font-size:0.85rem;'>{dorsal_txt}</div>
            </div>
            <div style='text-align:center; color:#888; font-size:0.75rem; margin-top:0.3rem;'>
                ▲ Portería rival &nbsp;·&nbsp; Portería propia ▼</div>
            """, unsafe_allow_html=True)

            # Perfil de dominio
            st.markdown("<div style='margin-top:1rem; color:#ccc; font-weight:700;'>Perfil de dominio</div>",
                        unsafe_allow_html=True)
            if pos_en == "Goalkeeper":
                indices = [
                    ("🧤 Paradas", pctl("Save Ratio %", row.get("Save Ratio %", 0) or 0)),
                    ("📤 Distribución", pctl("GK Successful Distribution p90", row.get("GK Successful Distribution p90", 0) or 0)),
                    ("✋ Seguridad", pctl("Catches p90", row.get("Catches p90", 0) or 0)),
                ]
            else:
                import numpy as np
                def idx(cols):
                    return round(np.mean([pctl(c, row.get(c, 0) or 0) for c in cols]), 0)
                indices = [
                    ("⚔️ Ataque", idx(["Goals p90", "Total Shots p90", "Successful Dribbles p90", "Total Touches In Opposition Box p90"])),
                    ("🎯 Control", idx(["Total Passes p90", "Pass Accuracy %", "Progressive Carries p90", "Key Passes (Attempt Assists) p90"])),
                    ("🛡️ Defensa", idx(["Tackles Won p90", "Interceptions p90", "Recoveries p90", "Duel Win %"])),
                ]
            for nombre_idx, val_idx in indices:
                col_barra = "#1a9e5a" if val_idx >= 66 else ("#e0a000" if val_idx >= 40 else "#d63030")
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:8px; margin:6px 0;'>
                    <div style='width:95px; font-size:0.9rem; color:#ddd;'>{nombre_idx}</div>
                    <div style='flex:1; background:rgba(255,255,255,0.12); border-radius:6px; height:18px;'>
                        <div style='width:{val_idx}%; background:{col_barra}; height:100%; border-radius:6px;'></div>
                    </div>
                    <div style='width:34px; text-align:right; font-weight:700; color:#fff;'>{val_idx:.0f}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_radar:
            r_vals = pcts + [pcts[0]]
            reales = [float(row.get(c, 0) or 0) for c, _, _, _, _ in kpis]
            reales_h = reales + [reales[0]]
            fig_ind = go.Figure()
            fig_ind.add_trace(go.Scatterpolar(
                r=r_vals, theta=etiquetas_kpi + [etiquetas_kpi[0]],
                fill="toself", name=row["nombre"],
                line=dict(color=ROJO if es_atleti else AZUL, width=2.5),
                fillcolor=f"rgba(204,32,32,0.22)" if es_atleti else "rgba(27,40,112,0.22)",
                customdata=[[rv] for rv in reales_h],
                hovertemplate="<b>%{theta}</b><br>valor: %{customdata[0]:.2f}<br>%{r:.0f}º percentil<extra></extra>"
            ))
            fig_ind.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10))),
                showlegend=False,
                title=dict(text=f"Percentiles vs {POS_ES.get(pos_en, pos_en)}s · 5 grandes ligas", x=0.5, font=dict(size=14)),
                height=430, margin=dict(t=50, b=30)
            )
            st.plotly_chart(fig_ind, use_container_width=True)

        # ───────── KEY STATS ─────────
        st.markdown("---")
        st.subheader("📊 Key Stats")
        gp = float(row.get("Games Played", 0) or 0)
        mins = float(row.get("Time Played", 0) or 0)
        goles = int(row.get("Goals", 0) or 0)
        asist = int(row.get("Goal Assists", 0) or 0)
        min_partido = mins / gp if gp > 0 else 0
        min_gol = mins / goles if goles > 0 else 0
        pass_acc = float(row.get("Pass Accuracy %", 0) or 0)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Partidos", f"{gp:.0f}")
        k2.metric("Minutos", f"{mins:.0f}")
        k3.metric("Goles", f"{goles}")
        k4.metric("Asistencias", f"{asist}")
        k5, k6, k7, k8 = st.columns(4)
        k5.metric("Min / partido", f"{min_partido:.0f}'")
        k6.metric("Min / gol", f"{min_gol:.0f}'" if goles > 0 else "—")
        k7.metric("% Acierto pase", f"{pass_acc:.1f}%")
        titular = float(row.get("Starts", 0) or 0)
        k8.metric("Titularidades", f"{titular:.0f}")

        # ───────── STRENGTHS / AREAS A MEJORAR ─────────
        st.markdown("---")
        resultados = []
        for i, (c, lab, sf, sd, inv) in enumerate(kpis):
            resultados.append((pcts[i], sf, sd))
        fortalezas = sorted([(p, sf) for p, sf, sd in resultados if p >= 65], reverse=True)
        debilidades = sorted([(p, sd) for p, sf, sd in resultados if p <= 35])

        col_f, col_d = st.columns(2)
        with col_f:
            st.markdown(f"<div style='color:#1a9e5a; font-size:1.2rem; font-weight:800;'>▲ Fortalezas "
                        f"<span style='background:#1a9e5a; color:#fff; border-radius:10px; padding:1px 9px; font-size:0.85rem;'>{len(fortalezas)}</span></div>",
                        unsafe_allow_html=True)
            if fortalezas:
                for p, t in fortalezas:
                    st.markdown(f"""
                    <div style='background:rgba(26,158,90,0.12); border-left:4px solid #1a9e5a;
                                padding:8px 12px; border-radius:6px; margin:5px 0; color:#eaeaea;'>
                        {t} <span style='float:right; color:#1a9e5a; font-weight:700;'>p{p:.0f}</span></div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Sin fortalezas destacadas (percentil ≥65) en este perfil.")

        with col_d:
            st.markdown(f"<div style='color:#d63030; font-size:1.2rem; font-weight:800;'>▼ Áreas a mejorar "
                        f"<span style='background:#d63030; color:#fff; border-radius:10px; padding:1px 9px; font-size:0.85rem;'>{len(debilidades)}</span></div>",
                        unsafe_allow_html=True)
            if debilidades:
                for p, t in debilidades:
                    st.markdown(f"""
                    <div style='background:rgba(214,48,48,0.12); border-left:4px solid #d63030;
                                padding:8px 12px; border-radius:6px; margin:5px 0; color:#eaeaea;'>
                        {t} <span style='float:right; color:#d63030; font-weight:700;'>p{p:.0f}</span></div>
                    """, unsafe_allow_html=True)
            else:
                st.caption("Sin debilidades marcadas (percentil ≤35) en este perfil.")

        st.caption("Percentiles calculados por 90 min frente a jugadores de la misma posición con ≥450 min en las 5 grandes ligas.")


# ══════════════════════════════════════════════
# PÁGINA 3.5: COMPARADOR DE JUGADORES
# ══════════════════════════════════════════════
elif pagina == "⚖️ Comparador":
    st.markdown('<div class="titulo-seccion">⚖️ Comparador de Jugadores — Radar interactivo</div>', unsafe_allow_html=True)
    st.markdown("Compara hasta **4 jugadores** de la base de datos por posición y descubre su perfil visual. "
                "Percentiles calculados por 90 min frente a jugadores de su misma posición en las **5 grandes ligas**.")

    # Paleta de colores por jugador
    PALETA = [AZUL, "#1a9e5a", ROJO, "#e07000"]

    def hex2rgba(h, a=0.12):
        """Convierte '#RRGGBB' a 'rgba(r,g,b,a)' (Plotly no acepta hex de 8 dígitos)."""
        h = h.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r},{g},{b},{a})"

    # Plantillas de KPIs por posición (columna, etiqueta, invertir)
    TEMPLATES = {
        "Delantero": [
            ("Goals p90", "Goles", False),
            ("Total Big Chances Scored p90", "Grandes ocasiones", False),
            ("Shots On Target ( inc goals ) p90", "Tiros a puerta", False),
            ("Total Shots p90", "Tiros totales", False),
            ("Total Touches In Opposition Box p90", "Toques área rival", False),
            ("Successful Dribbles p90", "Regates", False),
            ("Key Passes (Attempt Assists) p90", "Pases clave", False),
            ("Goal Assists p90", "Asistencias", False),
            ("Progressive Carries p90", "Conducciones prog.", False),
            ("Aerial Duels won p90", "Duelos aéreos gan.", False),
        ],
        "Centrocampista": [
            ("Total Passes p90", "Pases", False),
            ("Pass Accuracy %", "% Acierto pase", False),
            ("Key Passes (Attempt Assists) p90", "Pases clave", False),
            ("Shots Created p90", "Ocasiones creadas", False),
            ("Successful Dribbles p90", "Regates", False),
            ("Progressive Carries p90", "Conducciones prog.", False),
            ("Forward Passes p90", "Pases adelante", False),
            ("Interceptions p90", "Intercepciones", False),
            ("Tackles Won p90", "Entradas ganadas", False),
            ("Recoveries p90", "Recuperaciones", False),
        ],
        "Defensa": [
            ("Total Clearances p90", "Despejes", False),
            ("Interceptions p90", "Intercepciones", False),
            ("Total Tackles p90", "Entradas", False),
            ("Tackles Won p90", "Entradas ganadas", False),
            ("Aerial Duels won p90", "Duelos aéreos gan.", False),
            ("Aerial Win %", "% Aéreos", False),
            ("Blocks p90", "Bloqueos", False),
            ("Recoveries p90", "Recuperaciones", False),
            ("Duel Win %", "% Duelos", False),
            ("Pass Accuracy %", "% Acierto pase", False),
        ],
        "Portero": [
            ("Saves Made p90", "Paradas", False),
            ("Save Ratio %", "% Paradas", False),
            ("Saves Made from Inside Box p90", "Paradas área", False),
            ("Saves Made from Outside Box p90", "Paradas fuera", False),
            ("Penalties Saved p90", "Penaltis parados", False),
            ("Catches p90", "Blocadas", False),
            ("Punches p90", "Despejes puño", False),
            ("GK Successful Distribution p90", "Distribución OK", False),
            ("Pass Accuracy %", "% Acierto pase", False),
            ("Goals Conceded p90", "Goles encajados", True),
        ],
    }
    POS_MAP = {"Delantero": "Forward", "Centrocampista": "Midfielder",
               "Defensa": "Defender", "Portero": "Goalkeeper"}

    # ── Controles ──
    c1, c2 = st.columns([1, 2])
    with c1:
        plantilla_sel = st.selectbox("📋 Plantilla de comparación (posición):",
                                     list(TEMPLATES.keys()))
    pos_en = POS_MAP[plantilla_sel]
    kpis = TEMPLATES[plantilla_sel]

    # Pool de la posición (muestra fiable) para percentiles
    pool = cinco_ligas[(cinco_ligas["posicion"] == pos_en) &
                       (cinco_ligas["muestra_fiable"] == True)].copy().reset_index(drop=True)

    # Construir etiquetas únicas de jugador
    base_pos = cinco_ligas[cinco_ligas["posicion"] == pos_en].copy().reset_index(drop=True)
    etiquetas, mapa_idx, vistos = [], {}, {}
    for i, r in base_pos.iterrows():
        eq = "Atlético de Madrid" if r["equipo"] == "Club Atlético de Madrid" else r["equipo"]
        lab = f"{r['nombre']} · {eq}"
        if lab in vistos:
            lab = f"{lab} ({i})"
        vistos[lab] = i
        mapa_idx[lab] = i
        etiquetas.append(lab)
    base_pos["_label"] = etiquetas

    with c2:
        seleccion = st.multiselect(
            f"🔍 Selecciona jugadores ({plantilla_sel}, máx. 4):",
            etiquetas, max_selections=4,
            help="Escribe para buscar por nombre o club"
        )

    cc1, cc2 = st.columns(2)
    with cc1:
        modo = st.radio("Modo de visualización:", ["Percentiles", "Valores"], horizontal=True)
    with cc2:
        comparar_media = st.checkbox(f"Comparar con jugador mediano de {plantilla_sel.lower()}", value=False)

    if not seleccion:
        st.info("👆 Selecciona al menos un jugador para generar el radar de comparación.")
    else:
        etiquetas_kpi = [lab for _, lab, _ in kpis]

        # Función percentil dentro del pool de la posición
        def pct_pool(col, val, invert=False):
            s = pool[col].dropna()
            if len(s) == 0:
                return 50.0
            p = (s < val).mean() * 100
            return round(100 - p, 0) if invert else round(p, 0)

        # Recopilar datos de cada jugador
        jugadores_data = []
        for lab in seleccion:
            row = base_pos.loc[mapa_idx[lab]]
            valores_reales = [float(row.get(col, 0) or 0) for col, _, _ in kpis]
            percentiles = [pct_pool(col, row.get(col, 0) or 0, inv) for col, _, inv in kpis]
            eq = "Atlético de Madrid" if row["equipo"] == "Club Atlético de Madrid" else row["equipo"]
            mins = int(row.get("Time Played", 0) or 0)
            jugadores_data.append({"nombre": row["nombre"], "equipo": eq,
                                   "min": mins, "reales": valores_reales,
                                   "percentiles": percentiles})

        # Jugador mediano (opcional)
        if comparar_media:
            med_real = [float(pool[col].median()) for col, _, _ in kpis]
            med_pct = [pct_pool(col, pool[col].median(), inv) for col, _, inv in kpis]
            jugadores_data.append({"nombre": f"Mediano {plantilla_sel}", "equipo": "5 grandes ligas",
                                   "min": 0, "reales": med_real, "percentiles": med_pct})

        # ── Tarjetas de jugadores seleccionados ──
        cols_tar = st.columns(len(jugadores_data))
        for i, jd in enumerate(jugadores_data):
            col_j = PALETA[i % len(PALETA)] if jd["nombre"].startswith("Mediano") is False else "#888888"
            with cols_tar[i]:
                st.markdown(f"""
                <div style='border-left:5px solid {col_j}; background:rgba(255,255,255,0.06);
                            padding:0.5rem 0.8rem; border-radius:6px;'>
                    <b style='font-size:1.05rem;'>{jd['nombre']}</b><br>
                    <span style='font-size:0.82rem; opacity:0.85;'>{jd['equipo']}
                    {'· '+str(jd['min'])+' min' if jd['min']>0 else ''}</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("")

        # ── RADAR ──
        if modo == "Percentiles":
            datos_radar = [jd["percentiles"] for jd in jugadores_data]
            rango = [0, 100]
            sufijo_hover = "º percentil"
        else:
            # Normalizar valores a 0-100 sobre el máximo del pool (para escala comparable)
            maxes = []
            for col, _, _ in kpis:
                m = pool[col].max()
                maxes.append(m if m and m > 0 else 1)
            datos_radar = []
            for jd in jugadores_data:
                datos_radar.append([round(v / maxes[k] * 100, 1) for k, v in enumerate(jd["reales"])])
            rango = [0, 100]
            sufijo_hover = " (norm.)"

        fig_cmp = go.Figure()
        for i, jd in enumerate(jugadores_data):
            color = PALETA[i % len(PALETA)] if not jd["nombre"].startswith("Mediano") else "#888888"
            r_vals = datos_radar[i] + [datos_radar[i][0]]
            reales_hover = jd["reales"] + [jd["reales"][0]]
            fig_cmp.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=etiquetas_kpi + [etiquetas_kpi[0]],
                fill="toself",
                name=jd["nombre"],
                line=dict(color=color, width=2.5),
                fillcolor=hex2rgba(color, 0.12),
                customdata=[[rv] for rv in reales_hover],
                hovertemplate="<b>%{theta}</b><br>valor: %{customdata[0]:.2f}<br>" +
                              ("%{r:.0f}" + sufijo_hover if modo == "Percentiles" else "") + "<extra>" + jd["nombre"] + "</extra>"
            ))
        fig_cmp.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=rango, tickfont=dict(size=10))),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.12, xanchor="center", x=0.5),
            title=dict(text=f"Comparación por 90 min vs {plantilla_sel}s de las 5 grandes ligas", x=0.5),
            height=560, margin=dict(t=70, b=80)
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # ── TABLA DE COMPARACIÓN ──
        st.markdown("---")
        st.subheader(f"📋 Tabla de comparación — {modo}")
        if modo == "Percentiles":
            st.caption("Los percentiles indican la posición del jugador frente a otros (0 = peor, 100 = mejor). "
                       "Un 99 significa que supera al 99% de los jugadores de su posición.")

        tabla = {"Métrica (por 90 min)": etiquetas_kpi}
        for jd in jugadores_data:
            col_vals = jd["percentiles"] if modo == "Percentiles" else [round(v, 2) for v in jd["reales"]]
            tabla[f"{jd['nombre']}"] = col_vals
        df_tabla = pd.DataFrame(tabla)

        # Colorear: verde alto / rojo bajo (en percentiles por umbral; en valores por ranking de fila)
        cols_jug = [c for c in df_tabla.columns if c != "Métrica (por 90 min)"]

        def color_celda(val, fila_vals, es_pct):
            try:
                v = float(val)
            except (ValueError, TypeError):
                return ""
            if es_pct:
                if v >= 66:  return "color:#1a9e5a; font-weight:700;"
                if v <= 33:  return "color:#d63030; font-weight:700;"
                return "color:#cccccc;"
            else:
                vals = [float(x) for x in fila_vals]
                if len(set(vals)) == 1: return "color:#cccccc;"
                if v == max(vals): return "color:#1a9e5a; font-weight:700;"
                if v == min(vals): return "color:#d63030; font-weight:700;"
                return "color:#cccccc;"

        es_pct = (modo == "Percentiles")
        def estilo_fila(row):
            fila_vals = [row[c] for c in cols_jug]
            return [""] + [color_celda(row[c], fila_vals, es_pct) for c in cols_jug]

        styler = df_tabla.style.apply(estilo_fila, axis=1).format(
            {c: "{:.0f}" if es_pct else "{:.2f}" for c in cols_jug})
        st.dataframe(styler, use_container_width=True, hide_index=True, height=420)

        st.caption("🟢 Verde = valor alto/mejor · 🔴 Rojo = valor bajo/peor · ⚪ Gris = intermedio")


# ══════════════════════════════════════════════
# PÁGINA: FICHAJES OBJETIVO
# ══════════════════════════════════════════════
elif pagina == "🎯 Fichajes Objetivo":
    st.markdown('<div class="titulo-seccion">🎯 Fichajes Objetivo — Temporada 26/27</div>', unsafe_allow_html=True)
    st.markdown("Jugadores identificados por el motor de scouting como los más compatibles con el modelo de juego del Atleti, priorizando el rejuvenecimiento de la plantilla.")

    # Datos fichajes
    objetivos = [
        {"nombre":"T. Lemperle",   "club":"TSG Hoffenheim", "liga":"Bundesliga", "edad":24,
         "posicion":"Delantero",   "sim":99.3, "mv":"€15M", "coste":"€18M", "salario":"€2,5M/año",
         "reemplaza":"A. Sørloth",
         "descripcion":"Delantero centro alemán de 24 años. Reemplaza a Sørloth aportando juventud y proyección. 1.505 min en Bundesliga, 0.42 goles/90.",
         "kpis":{"Goals p90":0.42,"Shots on Target %":51.5,"Progressive Carries p90":3.59,"Duel Win %":46.0}},
        {"nombre":"M. Koné",       "club":"AS Roma",        "liga":"Serie A",    "edad":24,
         "posicion":"Centrocampista","sim":98.8,"mv":"€50M","coste":"€45M","salario":"€5M/año",
         "reemplaza":"Koke",
         "descripcion":"Centrocampista francés de 24 años. Sucesor natural de Koke. Titular indiscutible en Roma (2.302 min). 90.6% precisión de pase.",
         "kpis":{"Total Passes p90":49.07,"Pass Accuracy %":90.6,"Interceptions p90":0.63,"Duel Win %":50.7}},
        {"nombre":"Zé Pedro",      "club":"Cagliari Calcio","liga":"Serie A",    "edad":25,
         "posicion":"Defensor",    "sim":99.6,"mv":"€8M","coste":"€10M","salario":"€1,8M/año",
         "reemplaza":"J. Giménez",
         "descripcion":"Defensor polivalente de 25 años. Alternativa a Jacobo Ramón sin cláusulas Real Madrid. Asequible y con 1.284 min de titular.",
         "kpis":{"Duel Win %":50.4,"Aerial Win %":48.6,"Interceptions p90":0.87,"Pass Accuracy %":88.0}},
        {"nombre":"David Raya",    "club":"Arsenal FC",     "liga":"Premier L.", "edad":30,
         "posicion":"Portero",     "sim":99.4,"mv":"€35M","coste":"€35M","salario":"€6M/año",
         "reemplaza":"J. Oblak",
         "descripcion":"Portero español titular en Arsenal. Sucesor de Oblak. Internacional con España. 71.7% Save Ratio, 3.420 minutos.",
         "kpis":{"Save Ratio %":71.7,"Saves Made p90":2.7,"Pass Accuracy %":70.6}},
    ]

    for obj in objetivos:
        st.markdown(f"""
        <div class="jugador-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:1.4rem; font-weight:700; color:{AZUL};">{obj['nombre']}</span>
                    <span style="margin-left:10px; color:{ROJO}; font-weight:600;">{obj['posicion']}</span>
                </div>
                <div style="text-align:right;">
                    <span style="background:{ROJO}; color:white; padding:4px 12px; border-radius:12px; font-weight:600;">
                        Similitud: {obj['sim']}%
                    </span>
                </div>
            </div>
            <div style="color:#666; margin:0.5rem 0;">
                🏟️ {obj['club']} ({obj['liga']}) &nbsp;|&nbsp; 🎂 {obj['edad']} años &nbsp;|&nbsp;
                💰 VM: {obj['mv']} &nbsp;|&nbsp; 💸 Coste est.: {obj['coste']}
            </div>
            <p style="color:#444;">{obj['descripcion']}</p>
        </div>
        """, unsafe_allow_html=True)

        col_kpis = st.columns(len(obj["kpis"]))
        for i, (kpi, val) in enumerate(obj["kpis"].items()):
            with col_kpis[i]:
                st.metric(kpi.replace(" p90","").replace("_"," "), f"{val:.2f}")
        st.markdown("")

    # Comparativa radar: fichaje vs jugador a reemplazar
    st.markdown("---")
    st.subheader("📡 Comparativa: Fichaje vs Jugador a Reemplazar")
    fichaje_sel = st.selectbox("Selecciona fichaje para comparar:", [o["nombre"] for o in objetivos])
    obj_sel = next(o for o in objetivos if o["nombre"] == fichaje_sel)
    reemplazado = obj_sel["reemplaza"]

    st.markdown(f"**{obj_sel['nombre']}** ({obj_sel['edad']} años) ➡️ reemplaza a **{reemplazado}**")

    # KPIs del fichaje y del jugador reemplazado (mismos ejes)
    kpis_cmp = list(obj_sel["kpis"].keys())
    vals_fichaje = list(obj_sel["kpis"].values())

    fila_reemp = jugadores[jugadores["nombre"] == reemplazado]
    if not fila_reemp.empty:
        vals_reemp = [float(fila_reemp.iloc[0].get(k, 0)) for k in kpis_cmp]
    else:
        vals_reemp = [0]*len(kpis_cmp)

    # Normalizar cada KPI a escala 0-100 (según el máximo de la posición en las 5 ligas)
    pos_map = {"Delantero":"Forward","Centrocampista":"Midfielder","Defensor":"Defender","Portero":"Goalkeeper"}
    pos_en = pos_map.get(obj_sel["posicion"], "Forward")
    pool_pos = cinco_ligas[(cinco_ligas["posicion"]==pos_en) & (cinco_ligas["muestra_fiable"]==True)]
    vals_fichaje_norm, vals_reemp_norm = [], []
    for i, k in enumerate(kpis_cmp):
        maxv = pool_pos[k].max() if k in pool_pos.columns and pool_pos[k].max() > 0 else 1
        vals_fichaje_norm.append(round(vals_fichaje[i] / maxv * 100, 1))
        vals_reemp_norm.append(round(vals_reemp[i] / maxv * 100, 1))

    etiquetas_es = [k.replace(" p90","/90").replace("Goals","Goles").replace("Pass Accuracy","% Pase")
                     .replace("Total Passes","Pases").replace("Duel Win %","% Duelos")
                     .replace("Aerial Win %","% Aéreos").replace("Interceptions","Intercep.")
                     .replace("Shots on Target %","% Tiros Puerta").replace("Save Ratio %","% Paradas")
                     .replace("Saves Made","Paradas").replace("Progressive Carries","Conducciones")
                     for k in kpis_cmp]

    fig5 = go.Figure()
    # jugador a reemplazar (azul)
    fig5.add_trace(go.Scatterpolar(
        r=vals_reemp_norm + [vals_reemp_norm[0]], theta=etiquetas_es + [etiquetas_es[0]],
        fill="toself", name=f"{reemplazado} (actual)",
        line=dict(color=AZUL, width=2), fillcolor="rgba(27,40,112,0.2)"
    ))
    # fichaje objetivo (rojo)
    fig5.add_trace(go.Scatterpolar(
        r=vals_fichaje_norm + [vals_fichaje_norm[0]], theta=etiquetas_es + [etiquetas_es[0]],
        fill="toself", name=f"{obj_sel['nombre']} (objetivo)",
        line=dict(color=ROJO, width=2), fillcolor="rgba(204,32,32,0.25)"
    ))
    fig5.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        title=dict(text=f"{obj_sel['nombre']} vs {reemplazado} (normalizado 0-100)", x=0.5),
        height=420, showlegend=True
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Tabla comparativa de KPIs (valores reales)
    df_cmp = pd.DataFrame({
        "KPI": etiquetas_es,
        f"{reemplazado} (actual)": [round(v,2) for v in vals_reemp],
        f"{obj_sel['nombre']} (objetivo)": [round(v,2) for v in vals_fichaje],
    })
    df_cmp["Diferencia"] = (df_cmp[f"{obj_sel['nombre']} (objetivo)"] - df_cmp[f"{reemplazado} (actual)"]).round(2)
    df_cmp["Mejora"] = df_cmp["Diferencia"].apply(lambda x: "🟢" if x > 0 else "🔴" if x < 0 else "⚪")
    st.dataframe(df_cmp, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PÁGINA 5: ANÁLISIS FINANCIERO
# ══════════════════════════════════════════════
elif pagina == "💶 Análisis Financiero":
    st.markdown('<div class="titulo-seccion">💶 Análisis Financiero y Fair Play — 26/27</div>', unsafe_allow_html=True)

    # KPIs resumen
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Masa salarial actual", "€121,8M/año", delta=None)
    with col2:
        st.metric("Ahorro previsto 26/27", "-€21,6M/año",
                  delta="Griezmann + Koke (libres) + Sørloth", delta_color="inverse")
    with col3:
        st.metric("Coste neto traspasos", "€53M",
                  delta="Gasto €73M - Ingreso Sørloth €20M", delta_color="normal")
    with col4:
        st.metric("Masa salarial 26/27", "€109,5M/año",
                  delta="-€12,3M vs actual ✅", delta_color="inverse")

    st.success("✅ **FAIR PLAY OPERATIVO:** La operación reduce la masa salarial en €12,3M/año, cumpliendo los límites de La Liga y UEFA.")

    st.markdown("---")

    # Plantilla y salarios
    col_izq, col_der = st.columns([3, 2])

    with col_izq:
        st.subheader("💰 Masa salarial por jugador (plantilla principal)")
        df_sal = plantilla[plantilla["salario_anual_M"] > 0].sort_values("salario_anual_M", ascending=True)
        colores_sal = [ROJO if b == "SÍ (libre)" or b == "Posible venta"
                      else "#aaaaaa" if b == "YA SALIÓ"
                      else AZUL for b in df_sal["baja_probable"]]
        fig6 = go.Figure(go.Bar(
            y=df_sal["jugador"], x=df_sal["salario_anual_M"],
            orientation="h", marker_color=colores_sal,
            text=[f"€{v:.1f}M" for v in df_sal["salario_anual_M"]],
            textposition="outside"
        ))
        fig6.update_layout(
            title="Salario anual estimado (€M) — Rojo = salida prevista",
            xaxis_title="€ Millones/año", height=500,
            margin=dict(l=120, r=60)
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col_der:
        st.subheader("📋 Operaciones 26/27")
        st.markdown("**BAJAS PREVISTAS:**")
        salidas = plantilla[plantilla["baja_probable"].str.contains("SÍ|Posible", na=False)]
        for _, row in salidas.iterrows():
            color = "🔴" if "libre" in row["baja_probable"] else "💰"
            st.markdown(f"{color} **{row['jugador']}** — {row['baja_probable']} (ahorro: €{row['salario_anual_M']:.1f}M/año)")

        st.markdown("---")
        st.markdown("**ALTAS OBJETIVO:**")
        for _, row in financiero.head(3).iterrows():
            st.markdown(f"🟢 **{row['jugador']}** ({row['club']}) — Coste: €{row['coste_traspaso_M']}M | Salario: €{row['salario_estimado_M']}M/año")

        st.markdown("---")
        st.subheader("⚖️ Balance final")
        balance_data = {
            "Concepto": ["Salario Griezmann liberado","Salario Koke liberado",
                         "Salario Sørloth liberado","Ingreso venta Sørloth",
                         "Salario Lemperle (nuevo)","Salario Koné (nuevo)",
                         "Salario Zé Pedro (nuevo)","Traspaso Lemperle",
                         "Traspaso Koné","Traspaso Zé Pedro"],
            "Tipo": ["Ahorro","Ahorro","Ahorro","Ingreso","Gasto","Gasto","Gasto","Gasto","Gasto","Gasto"],
            "Importe (€M)": [9.4, 5.0, 7.2, 20.0, -2.5, -5.0, -1.8, -18.0, -45.0, -10.0]
        }
        df_bal = pd.DataFrame(balance_data)
        df_bal["Color"] = df_bal["Importe (€M)"].apply(lambda x: "🟢" if x > 0 else "🔴")
        st.dataframe(
            df_bal[["Color","Concepto","Importe (€M)"]].rename(columns={"Color":""}),
            use_container_width=True, hide_index=True
        )
        total = df_bal["Importe (€M)"].sum()
        st.markdown(f"**Balance neto: {'🟢' if total > 0 else '🔴'} €{total:.1f}M**")

    # ─────────────────────────────────────────────
    # ESCENARIO ESPECIAL: VENTA DE JULIÁN ÁLVAREZ
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.subheader("💎 Escenario estratégico: venta de Julián Álvarez")

    activar = st.checkbox("Activar análisis de venta de Julián Álvarez", value=False)

    st.markdown("""
    Julián Álvarez es el activo de mayor valor de la plantilla (valor de mercado ~€100M).
    El club valoraría su venta solo ante una oferta en torno a **€110-150M**, con interés reportado del FC Barcelona.
    Su salida liberaría una gran masa salarial y un fondo extraordinario para fichajes, pero supone perder
    al mejor finalizador del equipo, justo la debilidad detectada en el DAFO.
    """)

    if activar:
        precio_venta = st.slider("Precio de venta estimado (€M):", 90, 150, 110, 5)
        salario_julian = 7.0

        # Recalcular balance con la venta
        ingresos_base = 20.0      # venta Sørloth
        ahorro_base = 21.6        # Griezmann + Koke + Sørloth
        coste_traspasos_base = 73 # Lemperle + Koné + Zé Pedro
        salarios_nuevos = 2.5 + 5.0 + 1.8

        ingresos_total = ingresos_base + precio_venta
        ahorro_total = ahorro_base + salario_julian
        fondo_disponible = ingresos_total - coste_traspasos_base

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Ingreso por venta Julián", f"€{precio_venta}M")
        with c2:
            st.metric("Ingresos totales traspasos", f"€{ingresos_total:.0f}M",
                      delta="+Sørloth €20M")
        with c3:
            st.metric("Ahorro salarial total", f"-€{ahorro_total:.1f}M/año",
                      delta="+Julián €7M", delta_color="inverse")
        with c4:
            st.metric("Fondo libre tras 3 fichajes", f"€{fondo_disponible:.0f}M",
                      delta="para fichaje estrella", delta_color="normal")

        st.success(f"""
        ✅ **Reanálisis:** Vendiendo a Julián Álvarez por €{precio_venta}M, el club ingresa €{ingresos_total:.0f}M
        en traspasos y libera €{ahorro_total:.1f}M/año de masa salarial. Tras pagar los 3 fichajes de
        rejuvenecimiento (€73M), quedarían **€{fondo_disponible:.0f}M libres** para un delantero de primer nivel
        que sustituya su producción de gol.
        """)

        st.warning("""
        ⚠️ **Riesgo deportivo:** Julián Álvarez (8 goles, 4 asistencias, 0.51 goles/90 en todas las competiciones)
        es el mejor finalizador del equipo. El DAFO ya señalaba la conversión como punto débil del Atleti.
        Venderlo sin un reemplazo de garantía agravaría esa debilidad. La operación solo se recomienda si el
        fondo liberado (€{:.0f}M) se reinvierte en un '9' de élite.
        """.format(fondo_disponible))

        # Comparativa de escenarios
        st.markdown("**Comparativa de escenarios:**")
        comp = pd.DataFrame({
            "Escenario": ["Base (sin vender Julián)", "Con venta de Julián"],
            "Ingresos traspasos (€M)": [20, ingresos_total],
            "Ahorro salarial (€M/año)": [21.6, ahorro_total],
            "Fondo libre fichajes (€M)": [20-73, fondo_disponible],
            "Mejor finalizador": ["Se mantiene ✅", "Se pierde ⚠️"]
        })
        st.dataframe(comp, use_container_width=True, hide_index=True)
    else:
        st.info("Activa la casilla para ver el impacto financiero y deportivo de vender a Julián Álvarez.")
