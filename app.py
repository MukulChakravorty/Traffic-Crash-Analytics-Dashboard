import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# DATABASE CONNECTION

conn = sqlite3.connect("traffic_crash.db")

# SIDEBAR

st.sidebar.title("Dashboard Menu")
st.sidebar.write("Traffic Crash Analytics")

# DROPDOWN

selected_chart = st.sidebar.selectbox(

    "Select Analysis",

    [

        "Top Crash type",

        "Crash Hour Analysis",

        "Lighting Condition Analysis",

        "Top Dangerous Weather & Crash Type",
        
        "Top Injury Streets",

        "Injury Percentage by Crash Type",

        "Peak Crash Hour by Month",

        "Night-Time Crash Causes",

        "Daylight vs Darkness Injuries",

        "Traffic Control Device Analysis",

        "Crash Hotspot Locations",
        
        "Highest Injury Rate Streets",

        "Most Common Crash Type by Year",

        "Average Crashes Per Hour",

        "High-Risk Time Buckets",

        "Top 3 Crash Causes",

        "Year-over-Year Growth Rate",

        "Hotspot Zones"

        

    ]

)

# TITLE

st.title("Traffic Crash Analytics Dashboard")

# TOTAL CRASHES QUERY

query = """

SELECT COUNT(*) AS total_crashes
FROM CrashTable;

"""

df = pd.read_sql_query(query, conn)

# METRIC CARD

st.metric(

    label="Total Crash Records",

    value=df['total_crashes'][0]

)

# QUERY 2 → TOP CRASH TYPES

query2 = """

SELECT

    FIRST_CRASH_TYPE,

    COUNT(*) AS total_crashes

FROM CrashTable

GROUP BY FIRST_CRASH_TYPE

ORDER BY total_crashes DESC

LIMIT 10;

"""

df2 = pd.read_sql_query(query2, conn)

# QUERY 3 → CRASH HOUR ANALYSIS

query3 = """

SELECT

    CRASH_HOUR,

    COUNT(*) AS total_crashes

FROM CrashTable

GROUP BY CRASH_HOUR

ORDER BY CRASH_HOUR;

"""

df3 = pd.read_sql_query(query3, conn)

query4="""
SELECT
    LIGHTING_CONDITION,
    AVG(INJURIES_TOTAL) AS avg_injuries

FROM CrashTable

GROUP BY LIGHTING_CONDITION
ORDER BY avg_injuries DESC;

"""
df4=pd.read_sql(query4, conn)

#FROM HERE I AM INTEGRATING ALL THE ADVANCE_SQL QUERIES ON MY STREAMLIT PLATFORM::

#Q1=query5

query5="""
SELECT
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE,
    COUNT(*) AS total_crashes

FROM CrashTable

GROUP BY 
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE

ORDER BY total_crashes DESC

LIMIT 5;

"""
df5 = pd.read_sql_query(query5, conn)

query6="""
SELECT 

    STREET_NAME,
    COUNT(*) AS injury_crashes

FROM CrashTable

WHERE INJURIES_TOTAL>0

GROUP BY STREET_NAME
ORDER BY  injury_crashes DESC

LIMIT 10;
"""
df6=pd.read_sql(query6, conn)


query7= """

SELECT

FIRST_CRASH_TYPE,

COUNT(*) AS total_crashes,

SUM(

CASE

WHEN INJURIES_TOTAL > 0 THEN 1

ELSE 0

END

) AS injury_crashes,

ROUND(

SUM(

 CASE

 WHEN INJURIES_TOTAL > 0 THEN 1

 ELSE 0

END

) * 100.0 / COUNT(*),

2

) AS injury_percentage

FROM CrashTable

GROUP BY FIRST_CRASH_TYPE

ORDER BY injury_percentage DESC;

"""

df7 = pd.read_sql_query(query7, conn)


query8="""
WITH HourlyCrashes AS (

    SELECT

        SUBSTR(CRASH_DATE, 1, 2) AS crash_month,

        CRASH_HOUR,

        COUNT(*) AS total_crashes,

        ROW_NUMBER() OVER(

            PARTITION BY SUBSTR(CRASH_DATE, 1, 2)

            ORDER BY COUNT(*) DESC

        ) AS rank_num

    FROM CrashTable

    GROUP BY

        crash_month,
        CRASH_HOUR

)

SELECT

    crash_month,

    CRASH_HOUR,

    total_crashes

FROM HourlyCrashes

WHERE rank_num = 1

ORDER BY crash_month;

"""
df8=pd.read_sql(query8, conn)


query9="""
SELECT
    PRIM_CONTRIBUTORY_CAUSE,

    COUNT(*) AS total_crashes

FROM CrashTable

WHERE CRASH_HOUR >=18

GROUP BY PRIM_CONTRIBUTORY_CAUSE

ORDER BY total_crashes DESC

LIMIT 5;
"""
df9=pd.read_sql(query9, conn)



query10 = """

SELECT

    LIGHTING_CONDITION,

    AVG(INJURIES_TOTAL) AS avg_injuries

FROM CrashTable

WHERE LIGHTING_CONDITION IN (

    'DAYLIGHT',

    'DARKNESS'

)

GROUP BY LIGHTING_CONDITION

ORDER BY avg_injuries DESC;

"""

df10 = pd.read_sql(query10, conn)




query11="""
SELECT
TRAFFIC_CONTROL_DEVICE,
AVG(INJURIES_TOTAL) AS avg_injuries
FROM
Crashtable

GROUP BY TRAFFIC_CONTROL_DEVICE

ORDER BY avg_injuries DESC

LIMIT 10;
""" 
df11=pd.read_sql(query11, conn)

query12="""
SELECT
LATITUDE,
LONGITUDE,

COUNT(*)AS total_crashes

FROM
Crashtable

GROUP BY
LATITUDE,
LONGITUDE

ORDER BY total_crashes DESC

LIMIT 5;
"""
df12=pd.read_sql(query12,conn)

query13 = """

SELECT

    STREET_NAME,

    COUNT(*) AS total_crashes,

    SUM(INJURIES_TOTAL) AS total_injuries,

    ROUND(

        SUM(INJURIES_TOTAL) * 1.0 / COUNT(*),

        2

    ) AS injury_rate

FROM CrashTable

GROUP BY STREET_NAME

HAVING COUNT(*) > 100

ORDER BY injury_rate DESC

LIMIT 5;

"""

df13 = pd.read_sql_query(query13, conn)

query14="""
WITH RANKEDCRASHES AS(
    SELECT
        SUBSTR(CRASH_DATE, 7,4) AS crash_year,
        FIRST_CRASH_TYPE,
        count(*) AS total_crashes,


        ROW_NUMBER() OVER(
            PARTITION BY SUBSTR(CRASH_DATE, 7,4)
            ORDER BY COUNT(*) DESC
        ) AS rank_num

FROM Crashtable

GROUP BY

crash_year,
FIRST_CRASH_TYPE

)
SELECT 
    crash_year,
    FIRST_CRASH_TYPE,
    total_crashes

FROM RankedCrashes

WHERE rank_num = 1

ORDER BY crash_year;
"""
df14=pd.read_sql(query14, conn)

query15="""
SELECT 
CRASH_DAY_OF_WEEK,
COUNT(*) AS total_crashes,

ROUND(COUNT(*) * 1.0 / 24, 2) AS avg_crashes_per_hour
FROM Crashtable

GROUP BY CRASH_DAY_OF_WEEK
ORDER BY avg_crashes_per_hour DESC;
"""
df15=pd.read_sql(query15,conn)


query16="""
SELECT

CASE

WHEN CRASH_HOUR BETWEEN 6 AND 11 THEN 'MORNING'
WHEN CRASH_HOUR BETWEEN 12 AND 16 THEN 'AFTERNOON'
WHEN CRASH_HOUR BETWEEN 17 AND 20 THEN 'EVENING'

ELSE 'NIGHT'

END AS time_bucket,
SUM(INJURIES_TOTAL) AS total_injuries

FROM CrashTable
GROUP BY time_bucket

ORDER BY total_injuries DESC;
"""
df16=pd.read_sql(query16, conn)


query17="""
WITH  CauseRanking AS(
SELECT
FIRST_CRASH_TYPE,
PRIM_CONTRIBUTORY_CAUSE,

COUNT(*)AS total_crashes,

ROW_NUMBER() OVER(
PARTITION BY FIRST_CRASH_TYPE
ORDER BY COUNT(*) DESC
) AS rank_num

FROM Crashtable

GROUP BY
FIRST_CRASH_TYPE,
PRIM_CONTRIBUTORY_CAUSE

)
SELECT

FIRST_CRASH_TYPE,

PRIM_CONTRIBUTORY_CAUSE,

total_crashes,

rank_num

FROM CauseRanking

WHERE rank_num<=3

ORDER BY

FIRST_CRASH_TYPE,
rank_num;

"""
df17=pd.read_sql(query17,conn)

query18="""
SELECT
SUBSTR(CRASH_DATE,7,4) AS crash_year,
COUNT(*) AS total_crashes,

LAG (COUNT(*)) OVER (
ORDER BY SUBSTR(CRASH_DATE,7,4)
) AS previous_year_crashes,

ROUND(
(
COUNT(*)-
LAG(COUNT(*)) OVER(
ORDER BY SUBSTR(CRASH_DATE,7,4)
)

)*100.0 /
LAG (COUNT(*)) OVER (
ORDER BY SUBSTR(CRASH_DATE,7,4)
),
2
) AS growth_rate_percent

FROM CrashTable

GROUP BY crash_year

ORDER BY crash_year;
"""
df18=pd.read_sql(query18,conn)








query19="""
SELECT
ROUND(LATITUDE,2) AS zone_latitude,
ROUND(LONGITUDE, 2) AS zone_longitude,
COUNT(*)AS total_crashes

FROM CrashTable

GROUP BY

ROUND(LATITUDE,2),
ROUND(LONGITUDE, 2)

ORDER BY total_crashes DESC

LIMIT 10;

"""
df19=pd.read_sql(query19,conn)










































































# TOP CRASH TYPE SECTION

if selected_chart == "Top Crash type":

    st.subheader("Top Crash Type")

    st.dataframe(df2)

    st.subheader("Crash Type Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(df2['FIRST_CRASH_TYPE'], df2['total_crashes'])

    ax.set_title("Top Crash Types")

    st.pyplot(fig)

    st.markdown("""

Observation:

Parked Motor Vehicle crashes are the most common.
Rear-end collisions occur very frequently.
Turning and side-swipe crashes are also common.

Insight

Parking-related areas and traffic congestion appear to be major contributors to road accidents. 
Rear-end crashes also suggest insufficient following distance between vehicles.

""")

# CRASH HOUR ANALYSIS SECTION

if selected_chart == "Crash Hour Analysis":

    st.subheader("Crash Hour Analysis")

    st.dataframe(df3)
    
    st.subheader("Crash Hour Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(df3["CRASH_HOUR"], df3["total_crashes"])

    ax.set_title("Crash Hour Analysis")

    ax.set_xlabel("Crash Hour")

    ax.set_ylabel("Total Crashes")

    st.pyplot(fig)

    st.markdown("""
Observation

The highest number of crashes occurred at 3 PM (CRASH_HOUR = 15).
Crash frequency remains high between 3 PM and 5 PM.
Afternoon and evening hours show significantly more crashes compared to other times of the day.
Late-night and early-morning hours have comparatively fewer crashes.

Insight:

The increased number of crashes during afternoon and evening hours indicates that peak traffic congestion and office commuting periods contribute heavily to accident frequency. High vehicle density and driver fatigue may also play an important role.


""")

# LIGHTINGCONDITION ANALYSIS:

if selected_chart == "Lighting Condition Analysis":
    st.subheader("Lighting Condition Analysis")
    st.dataframe(df4)
    st.subheader("Lighting Condition Graph")

    fig, ax = plt.subplots(figsize=(10,5))
    
    ax.bar(df4['LIGHTING_CONDITION'], df4['avg_injuries'])

    ax.set_title("Lighting Condition vs Average Injuries")

    ax.set_xlabel("Lighting_Condition")
    ax.set_ylabel("Average Injuries")

    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("""

### Observation

- "Darkness, Lighted Road" conditions report the highest average injuries.
- Dawn and dusk periods also show relatively high injury severity.
- Daylight conditions have comparatively lower average injuries.
- Unknown lighting conditions report the lowest injury averages.

### Insight

- Reduced visibility during dark and transition-light conditions may increase crash severity.
- Proper street lighting and driver caution during dawn and dusk periods are critical for road safety.
- Improving night-time visibility and traffic awareness may help reduce injury risks.

""")
    
#Q1>Top Dangerous Weather & Crash Type

if selected_chart == "Top Dangerous Weather & Crash Type":

    st.subheader("Top Dangerous Weather + Crash Type")

    st.dataframe(df5)

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(

        df5['WEATHER_CONDITION']
        + " - " +
        df5['FIRST_CRASH_TYPE'],

        df5['total_crashes']

    )

    ax.set_title("Dangerous Weather & Crash Type")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Weather & Crash Type")

    st.pyplot(fig)

    st.markdown("""

     Insights

    - Most crashes occur during clear weather conditions.
    - Rear-end and parked vehicle crashes dominate the dataset.
    - Driver behavior contributes more heavily than weather alone.

    """)

#Q2>Top Injury Streets
if selected_chart=="Top Injury Streets":

    st.subheader("Top Injury Streets")

    st.dataframe(df6)

    st.subheader("Top Injury Streets Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(
        df6['STREET_NAME'],
        df6['injury_crashes']

    )

    ax.set_title("Top Injury Streets")

    ax.set_xlabel("Injury Crashes")

    ax.set_ylabel("Street Name")

    st.pyplot(fig)

    st.markdown("""

    ### OBSERVATION:
    
    WESTERN AVE has the highest number of injury crashes.
    PULASKI RD and ASHLAND AVE also report very high injury crash counts.
    Major urban roads dominate the top rankings.

    ### INSIGHTS:
    
    High-traffic arterial roads and busy intersections contribute heavily to injury-related crashes. These roads may require stricter traffic control and safety improvements.

""")
    
#Q3>percentage of crashes that resulted in injuries for each crash type. 

if selected_chart == "Injury Percentage by Crash Type":

    st.subheader("Injury Percentage by Crash Type")

    st.dataframe(df7)

    st.subheader("Injury Percentage Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(

        df7['FIRST_CRASH_TYPE'],

        df7['injury_percentage']


    )

    ax.set_title("Injury Percentage by Crash Type")

    ax.set_xlabel("Injury Percentage")

    ax.set_ylabel("Crash Type")

    st.pyplot(fig)

    st.markdown("""



### Observation

- Pedestrian crashes have the highest injury percentage.
- Pedalcyclist crashes also show high injury rates.
- Parked motor vehicle crashes have the lowest injury percentage.

### Insight

- Crash severity varies significantly by crash type.
- Vulnerable road users face the highest risk.

""")
    
#Q4> peak crash hour for each month.


if selected_chart == "Peak Crash Hour by Month":

    st.subheader("Peak Crash Hour by Month")

    st.dataframe(df8)

    st.subheader("Peak Crash Hour by Month Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(
        df8['crash_month'],
        df8['CRASH_HOUR'],
        marker="o"
    )

    ax.set_title("Peak Crash Hour by Month")

    ax.set_xlabel("Month")

    ax.set_ylabel("Peak Crash Hour")

    st.pyplot(fig)

    st.markdown("""

### Observation:

- Most months report peak crashes during 3 PM to 5 PM.
- Afternoon and evening traffic periods consistently show the highest crash frequency.

### Insight:

Rush-hour traffic and office commuting periods strongly influence crash occurrence patterns.

""")
    
#Q5>top 5 primary causes of crashes during night time (CRASH_HOUR ≥ 18). 

    
if selected_chart == "Night-Time Crash Causes":

    st.subheader("Night-Time Crash Causes")

    st.dataframe(df9)
    st.subheader("Night-Time Crash Causes Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(

        df9['PRIM_CONTRIBUTORY_CAUSE'],

        df9['total_crashes']

    )

    ax.set_title("Night-Time Crash Causes")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Crash Cause")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""

### Observation:

- "Unable to determine" is the major reported cause of accidents during night-time.
- Failing to yield right of way is the second most common cause of accidents.
- Failure to reduce speed is one of the major night-time crash causes.

### Insight:

- Driver attention and speed control become more critical during night hours.
- Better street lighting and stricter night traffic enforcement may reduce accidents.

""")

#Q6>average number of injuries in daylight vs darkness conditions. 

if selected_chart == "Daylight vs Darkness Injuries":

    st.subheader("Daylight vs Darkness Injuries")
    st.dataframe(df10)
    st.subheader("Daylight vs Darkness Injuries Graph")

    fig,ax= plt.subplots(figsize=(10,5))

    ax.bar(

        df10['LIGHTING_CONDITION'],
        df10['avg_injuries']
    )

    ax.set_title("Daylight vs Darkness Injuries")

    ax.set_xlabel("Lighting Condition")

    ax.set_ylabel("Average Injuries")

    st.pyplot(fig)

    st.markdown("""

### Observation:

- Darkness conditions show slightly higher average injuries compared to daylight conditions.
- Injury severity remains high during low-visibility driving conditions.
- Daylight conditions also contribute significantly to road injuries.

### Insight:

- Reduced visibility during darkness may increase crash severity and injury risk.
- Improved street lighting and cautious night-time driving can help reduce injuries.

""")
#Q7>traffic control device type has the highest average injuries per crash.  

if selected_chart =="Traffic Control Device Analysis":

    st.subheader("Traffic Control Device Analysis")

    st.dataframe(df11)

    st.subheader("Traffic Control Device Analysis Graph")

    fig,ax= plt.subplots(figsize=(10,5))

    ax.barh(
        df11['TRAFFIC_CONTROL_DEVICE'],
        df11['avg_injuries']
    )

    ax.set_title("Traffic Control Device Analysis")

    ax.set_xlabel("Average Injuries")

    ax.set_ylabel("Traffic Control Device")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Bicycle crossing signs show the highest average injuries per crash.
- Pedestrian crossing signs also report very high injury severity.
- Flashing control signals and yield signs contribute moderate average injuries.

### Insight

- Areas involving pedestrian and bicycle crossings are more vulnerable to severe injuries.
- Extra safety measures and better traffic awareness are needed around crossing zones.

""")

#Q8>top 5 locations (latitude/longitude) with the highest crash frequency. 

if selected_chart =="Crash Hotspot Locations":
    st.subheader("Crash Hotspot Locations") 
    st.dataframe(df12)
    st.subheader("Crash Hotspot Location's Graph") 
    fig,ax=plt.subplots(figsize=(10,5))

    locations = (

        df12['LATITUDE'].astype(str)

        + ", " +

        df12['LONGITUDE'].astype(str)
    )

    ax.barh(

        locations,

        df12['total_crashes']

    )
    ax.set_title("Crash Hotspot Locations")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Location")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Certain latitude and longitude combinations report extremely high crash frequency.
- Some hotspot locations show significantly higher crash counts compared to others.
- These locations likely represent busy intersections or high-traffic road segments.

### Insight

- High-crash locations should be prioritized for traffic monitoring and safety improvements.
- Better road planning, signal control, and traffic enforcement may help reduce accidents at hotspot zones.

""")
    
#Q9>

if selected_chart == "Highest Injury Rate Streets":
    st.subheader("Highest Injury Rate Streets")
    st.dataframe(df13)
    st.subheader("Highest Injury Rate Streets Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.barh(

        df13['STREET_NAME'],

        df13['injury_rate']

    )

    ax.set_title("Highest Injury Rate Streets")

    ax.set_xlabel("Injury Rate")

    ax.set_ylabel("Street Name")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- MARQUETTE DR reports the highest injury rate among streets with more than 100 crashes.
- FIFTH AVE and CORCORAN PL also show very high injury severity.
- Injury rates differ significantly across major street locations.

### Insight

- Certain streets may involve higher-speed traffic, risky intersections, or unsafe driving behavior.
- High injury-rate roads should be prioritized for traffic safety improvements and stricter monitoring.

""")

#Q10> most common crash type.
if selected_chart =="Most Common Crash Type by Year":
    st.subheader("Most Common Crash Type by Year")
    st.dataframe(df14)
    st.subheader("Most Common Crash Type by Years' Graph")
    fig, ax = plt.subplots(figsize=(10,5))

    labels =(

        df14['crash_year']

        + " - " +

        df14['FIRST_CRASH_TYPE']
    )
    ax.barh(

        labels,

        df14['total_crashes']
    )

    ax.set_title("Most Common Crash Type by Year")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Year & Crash Type")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Parked Motor Vehicle crashes remain the most common crash type across most years.
- Crash patterns appear highly consistent from 2020 to 2025.
- In 2026, Rear-End crashes become the most common crash category.

### Insight

- Repeated dominance of parked vehicle crashes suggests ongoing urban parking and traffic congestion issues.
- Long-term traffic planning and parking management strategies may help reduce recurring crash patterns.

""")

#Q11> day of the week with the highest average crashes per hour.

if selected_chart == "Average Crashes Per Hour":
    st.subheader("Average Crashes Per Hour")

    st.dataframe(df15)

    st.subheader("Average Crashes Per Hour Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(

        df15['CRASH_DAY_OF_WEEK'].astype(str),

        df15['avg_crashes_per_hour']

    )
    ax.set_title("Average Crashes Per Hour by Day")

    ax.set_xlabel("Day of Week")

    ax.set_ylabel("Average Crashes Per Hour")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Day 6 reports the highest average crashes per hour among all days of the week.
- Day 7 and Day 5 also show relatively high crash frequency.
- Crash activity varies noticeably across different days.

### Insight

- Certain days may experience heavier traffic movement, congestion, or increased travel activity.
- High-crash days should receive greater traffic monitoring and road safety attention.

""")


#Q12> Identify high-risk time slots:
#Group hours into buckets (Morning, Afternoon, Evening, Night)
#Find which bucket has the highest injury crashes


if selected_chart == "High-Risk Time Buckets":
    
    st.subheader("High-Risk Time Buckets")

    st.dataframe(df16)
    st.subheader("High-Risk Time Buckets Graph")

    fig,ax=plt.subplots(figsize=(10,5))

    ax.bar(
        
        df16['time_bucket'],
        df16['total_injuries']

    )

    ax.set_title("High-Risk Time Buckets")

    ax.set_xlabel("Time Bucket")

    ax.set_ylabel("Total Injuries")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Afternoon time slots report the highest number of injury crashes.
- Night and evening periods also show significantly high injury counts.
- Morning hours record comparatively lower crash injuries.

### Insight

- Heavy traffic movement during afternoon and evening hours may increase crash risks.
- Night-time visibility issues and driver fatigue may contribute to higher injury severity.
- High-risk time slots should receive stronger traffic monitoring and road safety enforcement.

""")


#Q13> Find the top 3 contributing causes for each crash type, (Use window functions like ROW_NUMBER() or RANK()).

if selected_chart== "Top 3 Crash Causes":

    st.subheader("Top 3 Crash Causes")
    st.dataframe(df17)
    st.subheader("Top 3 Crash Causes Graphical analysis")

    labels = df17['PRIM_CONTRIBUTORY_CAUSE']

    fig,ax=plt.subplots(figsize=(12,6))

    ax.barh(
        labels,
        df17['total_crashes']
    )
    ax.set_title("Top 3 Contributing Causes for Each Crash Type")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Crash Cause")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- "Unable to Determine" is the most common contributing cause across crash records.
- "Following Too Closely" and "Failing to Yield Right-of-Way" also report very high crash counts.
- Driver behavior-related causes dominate the major crash categories.

### Insight

- Many crashes may involve incomplete investigation details or unclear reporting conditions.
- Unsafe driving behavior such as tailgating and failure to follow traffic rules significantly contributes to accidents.
- Stronger traffic enforcement and driver awareness programs may help reduce recurring crash causes.

""")
    

#Calculate the year-over-year growth rate of crashes. (Use LAG() window function)


if selected_chart == "Year-over-Year Growth Rate":

    st.subheader("Year-over-Year Growth Rate")

    st.dataframe(df18)

    st.subheader("Year-over-Year Growth Rate Graph")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(

        df18['crash_year'],

        df18['growth_rate_percent'],

        marker='o'

    )

    ax.set_title("Year-over-Year Growth Rate of Crashes")

    ax.set_xlabel("Crash Year")

    ax.set_ylabel("Growth Rate (%)")

    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""

### Observation

- Crash growth rates fluctuate across different years.
- 2021 shows a strong positive growth in crash frequency.
- Crash growth remains relatively stable between 2022 and 2025.
- 2026 records a sharp negative growth rate compared to previous years.

### Insight

- Variations in yearly crash growth may be influenced by traffic volume, reporting patterns, or external conditions.
- The sharp decline in 2026 may indicate incomplete yearly data or reduced crash activity.
- Monitoring long-term growth trends can support better traffic planning and road safety strategies.

""")


#Q12>Identify hotspot zones:
#Group nearby locations (round latitude & longitude to 2 decimal places)
#Find top 10 zones with highest crashes


if selected_chart=="Hotspot Zones":
    st.subheader("Hotspot Zones")

    st.dataframe(df19)

    st.subheader("Hotspot Zones Graph")

    zones = (

        df19['zone_latitude'].astype(str)

        + ", " +

        df19['zone_longitude'].astype(str)

    )

    fig, ax = plt.subplots(figsize=(12,6))

    ax.barh(

        zones,

        df19['total_crashes']

    )

    ax.set_title("Top 10 Hotspot Zones")

    ax.set_xlabel("Total Crashes")

    ax.set_ylabel("Zone Location")

    plt.tight_layout()

    st.pyplot(fig)


    st.markdown("""

### Observation

- Certain hotspot zones report extremely high crash frequency compared to other areas.
- Nearby geographic locations combine into major high-risk traffic zones.
- Crash distribution is heavily concentrated in a few specific regions.

### Insight

- High-crash zones may represent busy intersections, highways, or densely populated urban roads.
- Traffic monitoring and infrastructure improvements should prioritize these hotspot regions.
- Geographic clustering analysis can help city planners identify accident-prone areas more effectively.

""")



























