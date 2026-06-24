import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='OptiFlow AI',layout='wide')
st.markdown('<style>.stApp{background:#0E1D34;color:white;}h1,h2,h3{color:#5DE2E7;}</style>',unsafe_allow_html=True)
st.title('🏭 OptiFlow AI')
st.caption('Intelligent Process Deviation Detection & Decision Support')

c1,c2=st.columns(2)
with c1:
    temp=st.slider('Kiln Temperature (°C)',1300,1500,1450)
    fuel=st.slider('Fuel Consumption (kg/t)',80,110,96)
    feed=st.slider('Feed Rate (TPH)',90,130,120)
    vib=st.slider('Vibration (mm/s)',0.0,10.0,3.0)
    energy=st.slider('Energy Consumption (kWh/t)',80,120,92)
run=st.button('🚀 Run AI Diagnosis')

if run:
    opt={'Kiln Temperature':1435,'Fuel Consumption':95,'Feed Rate':120,'Vibration':3,'Energy Consumption':92}
    cur={'Kiln Temperature':temp,'Fuel Consumption':fuel,'Feed Rate':feed,'Vibration':vib,'Energy Consumption':energy}
    score=100-int(abs(temp-1435)/3+abs(fuel-95)+abs(feed-120)+2*abs(vib-3)+abs(energy-92))
    score=max(40,min(score,100))
    with c2:
        st.metric('Plant Health Score',f'{score}/100')
        st.write('🟢 Healthy' if score>90 else '🟡 Warning' if score>75 else '🔴 Critical')
    rows=[]
    for k,v in cur.items():
        d=abs(v-opt[k])
        status='🟢 Normal' if d<3 else ('🟡 High' if d<8 else '🔴 Critical')
        rows.append([k,v,opt[k],status])
    st.dataframe(pd.DataFrame(rows,columns=['Parameter','Current','Optimal','Status']),use_container_width=True)
    st.subheader('🤖 AI Diagnosis')
    if temp>1450 and fuel>100:
        st.write('High kiln temperature and fuel consumption indicate inefficient combustion.')
        st.write('✓ Reduce kiln temperature by 15–20°C')
        st.write('✓ Inspect secondary air flow')
    elif vib>7:
        st.write('High vibration detected. Inspect rotating equipment.')
    elif energy>100:
        st.write('Energy consumption is above target. Optimize process settings.')
    else:
        st.write('Process is operating close to optimal conditions.')
    a,b,c,d=st.columns(4)
    a.metric('Energy Cost','↓ 8%')
    b.metric('Downtime','↓ 12%')
    c.metric('Stability','↑ 18%')
    d.metric('Decision Time','↓ 30%')
    fig=go.Figure()
    fig.add_bar(name='Current',x=list(cur.keys()),y=list(cur.values()))
    fig.add_bar(name='Optimal',x=list(opt.keys()),y=list(opt.values()))
    fig.update_layout(barmode='group',title='Current vs Optimal')
    st.plotly_chart(fig,use_container_width=True)
else:
    st.info('Adjust sliders and click Run AI Diagnosis.')
