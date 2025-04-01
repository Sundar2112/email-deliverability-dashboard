import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import json

# Set page configuration
st.set_page_config(page_title="Email Campaign Analytics", page_icon="📧", layout="wide")

# App title and description
st.title("Email Campaign Analytics Dashboard Generator")
st.markdown("Generate beautiful email campaign reports for multiple clients")

# Initialize session state for storing client data
if 'clients' not in st.session_state:
    st.session_state.clients = {}
    
# Function to load sample data
def load_sample_data():
    data = [
        {"Time":"2025-03-30","Sent":5609214,"Delivered":5406822,"Delivered %":96.39,"Opens":985875,"Opens %":18.23,"Clicks":4959,"Clicks %":0.09,"CTOR":0.5,"Bounces":202392,"Bounces %":3.61,"FBLs":0,"FBL %":0,"Unsubs":2204,"Unsub %":0.22},
        {"Time":"2025-03-29","Sent":16471605,"Delivered":15686999,"Delivered %":95.24,"Opens":2828680,"Opens %":18.03,"Clicks":6088,"Clicks %":0.04,"CTOR":0.22,"Bounces":784606,"Bounces %":4.76,"FBLs":0,"FBL %":0,"Unsubs":4710,"Unsub %":0.17},
        {"Time":"2025-03-28","Sent":1000000,"Delivered":979801,"Delivered %":97.98,"Opens":341232,"Opens %":34.83,"Clicks":1205,"Clicks %":0.12,"CTOR":0.35,"Bounces":20199,"Bounces %":2.02,"FBLs":0,"FBL %":0,"Unsubs":619,"Unsub %":0.18},
        {"Time":"2025-03-23","Sent":40000126,"Delivered":38603547,"Delivered %":96.51,"Opens":7444887,"Opens %":19.29,"Clicks":20943,"Clicks %":0.05,"CTOR":0.28,"Bounces":1396579,"Bounces %":3.49,"FBLs":0,"FBL %":0,"Unsubs":30013,"Unsub %":0.4},
        {"Time":"2025-03-22","Sent":3000000,"Delivered":2959263,"Delivered %":98.64,"Opens":1400042,"Opens %":47.31,"Clicks":4150,"Clicks %":0.14,"CTOR":0.3,"Bounces":40737,"Bounces %":1.36,"FBLs":0,"FBL %":0,"Unsubs":3072,"Unsub %":0.22},
        {"Time":"2025-03-21","Sent":298164,"Delivered":290801,"Delivered %":97.53,"Opens":152051,"Opens %":52.29,"Clicks":268,"Clicks %":0.09,"CTOR":0.18,"Bounces":7363,"Bounces %":2.47,"FBLs":0,"FBL %":0,"Unsubs":223,"Unsub %":0.15},
        {"Time":"2025-03-19","Sent":250000,"Delivered":248404,"Delivered %":99.36,"Opens":164270,"Opens %":66.13,"Clicks":248,"Clicks %":0.1,"CTOR":0.15,"Bounces":1596,"Bounces %":0.64,"FBLs":0,"FBL %":0,"Unsubs":379,"Unsub %":0.23},
        {"Time":"2025-03-18","Sent":16628568,"Delivered":15642025,"Delivered %":94.07,"Opens":1798527,"Opens %":11.5,"Clicks":89922,"Clicks %":0.57,"CTOR":5,"Bounces":986543,"Bounces %":5.93,"FBLs":0,"FBL %":0,"Unsubs":7355,"Unsub %":0.41},
        {"Time":"2025-03-16","Sent":33630,"Delivered":32945,"Delivered %":97.96,"Opens":6158,"Opens %":18.69,"Clicks":15,"Clicks %":0.05,"CTOR":0.24,"Bounces":685,"Bounces %":2.04,"FBLs":0,"FBL %":0,"Unsubs":7,"Unsub %":0.11},
        {"Time":"2025-03-15","Sent":11966683,"Delivered":11286750,"Delivered %":94.32,"Opens":1733614,"Opens %":15.36,"Clicks":2767,"Clicks %":0.02,"CTOR":0.16,"Bounces":679933,"Bounces %":5.68,"FBLs":0,"FBL %":0,"Unsubs":3933,"Unsub %":0.23},
        {"Time":"2025-03-14","Sent":40000000,"Delivered":38416792,"Delivered %":96.04,"Opens":5147386,"Opens %":13.4,"Clicks":22558,"Clicks %":0.06,"CTOR":0.44,"Bounces":1583208,"Bounces %":3.96,"FBLs":0,"FBL %":0,"Unsubs":18857,"Unsub %":0.37},
        {"Time":"2025-03-12","Sent":12837081,"Delivered":12099949,"Delivered %":94.26,"Opens":1748925,"Opens %":14.45,"Clicks":3005,"Clicks %":0.02,"CTOR":0.17,"Bounces":737132,"Bounces %":5.74,"FBLs":0,"FBL %":0,"Unsubs":3669,"Unsub %":0.21},
        {"Time":"2025-03-10","Sent":10000,"Delivered":9819,"Delivered %":98.19,"Opens":3924,"Opens %":39.96,"Clicks":10,"Clicks %":0.1,"CTOR":0.25,"Bounces":181,"Bounces %":1.81,"FBLs":0,"FBL %":0,"Unsubs":6,"Unsub %":0.15},
        {"Time":"2025-03-09","Sent":50000100,"Delivered":48059921,"Delivered %":96.12,"Opens":8039586,"Opens %":16.73,"Clicks":38519,"Clicks %":0.08,"CTOR":0.48,"Bounces":1940179,"Bounces %":3.88,"FBLs":1,"FBL %":0,"Unsubs":30413,"Unsub %":0.38},
        {"Time":"2025-03-08","Sent":41514131,"Delivered":39668043,"Delivered %":95.55,"Opens":6785699,"Opens %":17.11,"Clicks":14855,"Clicks %":0.04,"CTOR":0.22,"Bounces":1846088,"Bounces %":4.45,"FBLs":0,"FBL %":0,"Unsubs":20679,"Unsub %":0.3},
        {"Time":"2025-03-05","Sent":12970603,"Delivered":12230358,"Delivered %":94.29,"Opens":1570310,"Opens %":12.84,"Clicks":2804,"Clicks %":0.02,"CTOR":0.18,"Bounces":740245,"Bounces %":5.71,"FBLs":0,"FBL %":0,"Unsubs":3570,"Unsub %":0.23}
    ]
    return pd.DataFrame(data)

# Function to parse CSV files
def parse_csv(file):
    # Print column names to debug
    data = pd.read_csv(file)
    print(f"Original columns: {data.columns.tolist()}")
    
    # Strip whitespace from column names
    data.columns = data.columns.str.strip()
    print(f"After stripping whitespace: {data.columns.tolist()}")
    
    # Replace any non-ASCII characters
    data.columns = [c.encode('ascii', 'replace').decode('ascii') for c in data.columns]
    print(f"After fixing encoding: {data.columns.tolist()}")
    
    return data

# Function to calculate key metrics
def calculate_metrics(df):
    # Convert percentage strings to float if needed
    for col in df.columns:
        if "%" in col:
            if df[col].dtype == object:
                df[col] = df[col].str.replace('%', '').astype(float)
    
    # Sort data chronologically
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values('Time')
    
    # Calculate totals
    total_sent = df['Sent'].sum()
    total_delivered = df['Delivered'].sum()
    total_opens = df['Opens'].sum()
    total_clicks = df['Clicks'].sum()
    total_bounces = df['Bounces'].sum()
    total_unsubs = df['Unsubs'].sum()
    
    # Calculate average rates
    avg_delivery_rate = (total_delivered / total_sent * 100).round(2)
    avg_open_rate = (total_opens / total_delivered * 100).round(2)
    avg_click_rate = (total_clicks / total_delivered * 100).round(2)
    avg_ctor = (total_clicks / total_opens * 100).round(2)
    avg_bounce_rate = (total_bounces / total_sent * 100).round(2)
    avg_unsub_rate = (total_unsubs / total_delivered * 100).round(2)
    
    metrics = {
        'total_sent': total_sent,
        'total_delivered': total_delivered,
        'total_opens': total_opens,
        'total_clicks': total_clicks,
        'total_bounces': total_bounces,
        'total_unsubs': total_unsubs,
        'avg_delivery_rate': avg_delivery_rate,
        'avg_open_rate': avg_open_rate,
        'avg_click_rate': avg_click_rate,
        'avg_ctor': avg_ctor,
        'avg_bounce_rate': avg_bounce_rate,
        'avg_unsub_rate': avg_unsub_rate
    }
    
    return metrics

# Function to generate insights based on metrics and data
def generate_insights(df, metrics):
    insights = []
    
    # Sort data chronologically
    df['Time'] = pd.to_datetime(df['Time'])
    df = df.sort_values('Time')
    
    # Find days with highest engagement
    best_open_day = df.loc[df['Opens %'].idxmax()]
    best_click_day = df.loc[df['Clicks %'].idxmax()]
    best_ctor_day = df.loc[df['CTOR'].idxmax()]
    
    # Find days with lowest bounce rates
    lowest_bounce_day = df.loc[df['Bounces %'].idxmin()]
    
    # Calculate variability in metrics
    open_rate_std = df['Opens %'].std()
    click_rate_std = df['Clicks %'].std()
    
    # Generate insights
    insights.append(f"Overall delivery rate is {metrics['avg_delivery_rate']}%, suggesting good list quality")
    
    if metrics['avg_open_rate'] > 20:
        insights.append(f"Average open rate of {metrics['avg_open_rate']}% is excellent, above industry average")
    elif metrics['avg_open_rate'] > 15:
        insights.append(f"Average open rate of {metrics['avg_open_rate']}% is good, around industry average")
    else:
        insights.append(f"Average open rate of {metrics['avg_open_rate']}% has room for improvement")
    
    insights.append(f"Highest engagement on {best_open_day['Time'].strftime('%b %d')} with a {best_open_day['Opens %']}% open rate")
    
    if best_click_day['Clicks %'] > 0.2:
        insights.append(f"Best click performance on {best_click_day['Time'].strftime('%b %d')} with {best_click_day['Clicks %']}% click rate")
    
    if open_rate_std > 10:
        insights.append(f"High variability in open rates (std: {open_rate_std:.2f}%), suggests inconsistent email quality or audience targeting")
    
    # Check for campaigns with unusual success
    unusual_success = df[(df['Opens %'] > df['Opens %'].mean() + df['Opens %'].std()) | 
                          (df['Clicks %'] > df['Clicks %'].mean() + df['Clicks %'].std())]
    
    if not unusual_success.empty:
        for _, row in unusual_success.iterrows():
            if row['Opens %'] > df['Opens %'].mean() + df['Opens %'].std():
                insights.append(f"Campaign on {row['Time'].strftime('%b %d')} had unusually high open rate ({row['Opens %']}%)")
            if row['Clicks %'] > df['Clicks %'].mean() + df['Clicks %'].std():
                insights.append(f"Campaign on {row['Time'].strftime('%b %d')} had unusually high click rate ({row['Clicks %']}%)")
    
    return insights

# Function to generate recommendations based on insights and metrics
def generate_recommendations(df, metrics, insights):
    recommendations = []
    
    # Basic recommendations based on metrics
    if metrics['avg_open_rate'] < 20:
        recommendations.append("Improve subject lines through A/B testing to increase open rates")
    
    if metrics['avg_click_rate'] < 0.1:
        recommendations.append("Review content strategy to improve click-through rates")
        recommendations.append("Ensure email content aligns with subject line promises")
    
    if metrics['avg_bounce_rate'] > 3:
        recommendations.append("Review email list quality and remove invalid or inactive addresses")
    
    # Look for successful campaigns
    high_performing = df[(df['Opens %'] > df['Opens %'].mean() + df['Opens %'].std()) | 
                         (df['Clicks %'] > df['Clicks %'].mean() + df['Clicks %'].std())]
    
    if not high_performing.empty:
        dates = [date.strftime('%b %d') for date in high_performing['Time']]
        date_str = ", ".join(dates)
        recommendations.append(f"Analyze successful campaigns ({date_str}) to identify effective elements")
    
    # Volume-based recommendations
    large_campaigns = df[df['Sent'] > df['Sent'].mean()]
    if not large_campaigns.empty and metrics['avg_open_rate'] < 20:
        recommendations.append("Consider segment-specific campaigns instead of mass emails for better engagement")
    
    # Add more personalized recommendations
    recommendations.append("Implement re-engagement campaigns for inactive subscribers")
    recommendations.append("Test different send times to optimize for higher open rates")
    recommendations.append("Enhance mobile responsiveness of email templates")
    recommendations.append("Add personalization to improve recipient engagement")
    
    return recommendations

# Function to create key metrics cards
def create_metrics_section(metrics):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Emails", f"{metrics['total_sent']:,}")
    with col2:
        st.metric("Delivery Rate", f"{metrics['avg_delivery_rate']}%")
    with col3:
        st.metric("Open Rate", f"{metrics['avg_open_rate']}%")
    with col4:
        st.metric("Click Rate", f"{metrics['avg_click_rate']}%")
    with col5:
        st.metric("CTOR", f"{metrics['avg_ctor']}%")
    with col6:
        st.metric("Bounce Rate", f"{metrics['avg_bounce_rate']}%")

# Function to create engagement pie chart
def create_engagement_chart(metrics):
    labels = ['Opened & Clicked', 'Opened (No Click)', 'Not Opened', 'Bounced']
    values = [
        metrics['total_clicks'],
        metrics['total_opens'] - metrics['total_clicks'],
        metrics['total_delivered'] - metrics['total_opens'],
        metrics['total_bounces']
    ]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker_colors=['#00C49F', '#0088FE', '#FFBB28', '#FF8042']
    )])
    
    fig.update_layout(
        title_text="Email Engagement Breakdown",
        height=400,
    )
    
    return fig

# Function to create volume chart
def create_volume_chart(df):
    df_sorted = df.sort_values('Time')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_sorted['Time'],
        y=df_sorted['Sent'],
        name='Sent',
        marker_color='rgba(136, 132, 216, 0.8)'
    ))
    
    fig.add_trace(go.Bar(
        x=df_sorted['Time'],
        y=df_sorted['Delivered'],
        name='Delivered',
        marker_color='rgba(130, 202, 157, 0.8)'
    ))
    
    fig.update_layout(
        title_text="Daily Campaign Volume",
        xaxis_title="Date",
        yaxis_title="Number of Emails",
        barmode='group',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Function to create rate trends chart
def create_rate_trends(df):
    df_sorted = df.sort_values('Time')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Delivered %'],
        mode='lines+markers',
        name='Delivery Rate',
        line=dict(color='rgba(136, 132, 216, 0.8)', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Opens %'],
        mode='lines+markers',
        name='Open Rate',
        line=dict(color='rgba(130, 202, 157, 0.8)', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Clicks %'],
        mode='lines+markers',
        name='Click Rate',
        line=dict(color='rgba(255, 198, 88, 0.8)', width=3)
    ))
    
    fig.update_layout(
        title_text="Key Metrics Trend",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Function to create engagement rate trends
def create_engagement_trends(df):
    df_sorted = df.sort_values('Time')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Opens %'],
        mode='lines+markers',
        name='Open Rate',
        line=dict(color='rgba(136, 132, 216, 0.8)', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['CTOR'],
        mode='lines+markers',
        name='CTOR',
        line=dict(color='rgba(130, 202, 157, 0.8)', width=3)
    ))
    
    fig.update_layout(
        title_text="Engagement Rate Trend",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Function to create negative metrics trends
def create_negative_trends(df):
    df_sorted = df.sort_values('Time')
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Bounces %'],
        mode='lines+markers',
        name='Bounce Rate',
        line=dict(color='rgba(255, 115, 0, 0.8)', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_sorted['Time'],
        y=df_sorted['Unsub %'],
        mode='lines+markers',
        name='Unsubscribe Rate',
        line=dict(color='rgba(255, 0, 0, 0.8)', width=3)
    ))
    
    fig.update_layout(
        title_text="Negative Metrics Trend",
        xaxis_title="Date",
        yaxis_title="Rate (%)",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

# Function to display insights and recommendations
def display_insights(insights, recommendations):
    st.subheader("Key Insights")
    for i, insight in enumerate(insights[:5]):
        st.markdown(f"- {insight}")
    
    st.subheader("Recommendations")
    for i, recommendation in enumerate(recommendations[:5]):
        st.markdown(f"- {recommendation}")

# Function to create a PDF report
def create_downloadable_report():
    # In a real app, you would generate a PDF here
    # For this example, we'll just create a text summary
    buffer = io.BytesIO()
    buffer.write(b"Email Campaign Analytics Report\n\n")
    buffer.write(b"Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode() + b"\n\n")
    
    # In a real implementation, you would add charts and metrics to the PDF
    
    buffer.seek(0)
    return buffer

# Function to display the dashboard for a specific client
def display_client_dashboard(client_name, df):
    st.header(f"Email Campaign Dashboard - {client_name}")
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
    # Generate insights and recommendations
    insights = generate_insights(df, metrics)
    recommendations = generate_recommendations(df, metrics, insights)
    
    # Display time period
    min_date = df['Time'].min().strftime('%b %d, %Y')
    max_date = df['Time'].max().strftime('%b %d, %Y')
    st.subheader(f"Period: {min_date} to {max_date}")
    
    # Create metrics section
    create_metrics_section(metrics)
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_engagement_chart(metrics), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_volume_chart(df), use_container_width=True)
    
    st.plotly_chart(create_rate_trends(df), use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.plotly_chart(create_engagement_trends(df), use_container_width=True)
    
    with col4:
        st.plotly_chart(create_negative_trends(df), use_container_width=True)
    
    # Display insights and recommendations
    st.subheader("Analysis")
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### Key Insights")
        for insight in insights[:5]:
            st.markdown(f"- {insight}")
    
    with col6:
        st.markdown("#### Recommendations")
        for recommendation in recommendations[:5]:
            st.markdown(f"- {recommendation}")
    
    # Raw data display option
    with st.expander("View Raw Data"):
        st.dataframe(df)
    
    # Download report button
    report = create_downloadable_report()
    st.download_button(
        label="Download PDF Report",
        data=report,
        file_name=f"{client_name}_email_report_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

# Function to save client data
def save_client_data(client_name, df):
    st.session_state.clients[client_name] = df
    
    # Display success message
    st.success(f"Data for {client_name} successfully saved!")

# Function to create batch reports
def create_batch_reports():
    if len(st.session_state.clients) == 0:
        st.warning("No client data available. Please add at least one client first.")
        return
    
    st.subheader("Generate Batch Reports")
    st.write(f"You have {len(st.session_state.clients)} clients available for batch processing.")
    
    # Select clients for batch processing
    selected_clients = st.multiselect("Select clients for batch report generation:", 
                                    list(st.session_state.clients.keys()),
                                    default=list(st.session_state.clients.keys()))
    
    if st.button("Generate Batch Reports"):
        if len(selected_clients) > 0:
            st.info(f"Generating reports for {len(selected_clients)} clients...")
            
            # In a real application, this would generate and save reports for each client
            # For this example, we'll just show a progress bar
            progress_bar = st.progress(0)
            for i, client in enumerate(selected_clients):
                # Simulate report generation
                # In a real app, you would call a function to generate and save the report
                progress_bar.progress((i + 1) / len(selected_clients))
                st.write(f"Generated report for {client}")
            
            st.success("Batch report generation complete!")
        else:
            st.warning("Please select at least one client for batch processing.")

# Main app layout
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Client Dashboard", "Add New Client", "Batch Reports"])
    
if page == "Client Dashboard":
    if len(st.session_state.clients) == 0:
        st.info("No clients added yet. Use the 'Add New Client' page to add client data.")
    else:
        # Show dropdown to select client
        selected_client = st.sidebar.selectbox("Select a client:", list(st.session_state.clients.keys()))
        
        # Add debug information
        st.sidebar.write("Debug info:")
        client_df = st.session_state.clients[selected_client]
        st.sidebar.write(f"Columns in dataset: {client_df.columns.tolist()}")
        
        try:
            display_client_dashboard(selected_client, client_df)
        except Exception as e:
            st.error(f"Error displaying dashboard: {str(e)}")
            st.write("Please try uploading your data again.")
    
    elif page == "Add New Client":
        st.header("Add New Client Data")
        
        # Client name input
        client_name = st.text_input("Client Name")
        
        # Method selection
        upload_method = st.radio("Select data input method:", ["Upload CSV", "Load Sample Data"])
        
        df = None
        
        if upload_method == "Upload CSV":
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                try:
                    df = parse_csv(uploaded_file)
                    st.success("File uploaded successfully!")
                    st.dataframe(df.head())
                except Exception as e:
                    st.error(f"Error parsing file: {e}")
        else:
            # Load sample data
            if st.button("Load Sample Data"):
                df = load_sample_data()
                st.success("Sample data loaded successfully!")
                st.dataframe(df.head())
        
        # Save client data
        if df is not None and client_name:
            if st.button("Save Client Data"):
                save_client_data(client_name, df)
                st.success("Client data saved! View the dashboard on the 'Client Dashboard' page.")
        elif df is not None and not client_name:
            st.warning("Please enter a client name to save the data.")
    
    elif page == "Batch Reports":
        st.header("Batch Report Generation")
        create_batch_reports()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        This application automatically generates email campaign analytics reports for multiple clients.
        Upload your data, view dashboards, and create batch reports.
        """
    )

if __name__ == "__main__":
    main()
