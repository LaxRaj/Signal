# **📡 Project Signal: Finding the Future, Faster.**

Hey there\! I'm Lakshyaraj, a CS student who's always been fascinated by the intersection of technology and finance. I noticed something crazy: the people whose job it is to find the next big thing—Venture Capitalists—spend hours every day just manually scrolling through news sites. It felt like they were panning for gold with a teaspoon.

I thought, "What if we could build a metal detector?"

That's the origin of **Project Signal**. It's my attempt to build an intelligent engine that automatically sifts through the daily noise of the internet to find the real signals—the startups and tech trends that are actually worth paying attention to.

### **Demo: The "Morning Briefing" Dashboard**

Here's a quick look at the "Time Machine" mode in action. Instead of spending hours reading, a VC could see this in minutes.



## **The "How": Deconstructing the Hype**

So, how does it work? I realized that to think like a VC, the app needed to answer three core questions for every piece of news it found. I turned this logic into the **"Signal Score"**, a smart algorithm that rates every opportunity.

### **1\. What's the Event? (The *Content Score*)**

Not all news is equal. A funding announcement is a massive vote of confidence from other smart investors. A product launch shows a team can actually build. A partnership shows business savvy. The Signal Score weighs a funding round highest because it's the strongest proof of external validation.

### **2\. Who's Talking? (The *Source Score*)**

Credibility matters. A feature in a curated outlet like **TechCrunch** means an editor vetted the story—that's a strong signal. A top spot on **Product Hunt** means the tech community itself is excited—a different, but equally powerful, grassroots signal. The score knows the difference.

### **3\. How Deep is the Tech? (The *AI Confidence Score*)**

In today's world, everyone says they use "AI". I wanted to go deeper. The app uses a keyword matrix to differentiate between a company that just uses "AI-powered" as a buzzword versus one that is building with "LLMs," "foundational models," or "neural networks." This helps find the companies with a real, defensible tech advantage.

## **The Result: From a Score to a Strategy**

The raw score is then translated into simple, actionable tiers that tell a VC exactly what to do:

* 🔴 **Priority Review (Score \> 85):** "Drop everything. This is a must-see."  
* 🟠 **Emerging Trend (Score 70-84):** "Interesting. Let's look into this this week."  
* 🔵 **Monitor (Score 50-69):** "Good to know. Let's keep an eye on it."

## **Killer Features**

* **🤖 AI Analyst Take:** I integrated the Gemini API to provide a "VC Analyst Take" on any selected company, instantly generating a qualitative summary of its potential and risks.  
* **🕰️ The Time Machine:** The app can load two years of historical data. With a simple slider, you can go back in time and see what signals were firing on any given day.  
* **💰 ROI Simulator:** This is the best part. After you "time travel" and find a promising startup from the past, you can click "Simulate Investment" to see what the real-world financial outcome was. It's a direct way to prove that the signals actually lead to real returns.

## **Tech Stack**

* **Backend & Data Analysis:** Python, Pandas  
* **Web Framework:** Streamlit  
* **Data Scraping:** Requests, BeautifulSoup4  
* **NLP (for company recognition):** spaCy  
* **AI Analyst:** Gemini API

## **Getting Started Locally**

Super pumped for you to try this out\! Here’s how to get it running.

1. **Clone the repo:**  
   git clone https://github.com/LaxRaj/Signal
   cd project\_signal

2. **Set up your virtual environment:**  
   python3 \-m venv venv  
   source venv/bin/activate

3. **Install the goods:**  
   pip install \-r requirements.txt

4. **Download the NLP model:**  
   python \-m spacy download en\_core\_web\_sm

5. **Run it\!**  
   streamlit run app.py

   Your browser should open up with the app running.

## **What's Next?**

This project was an incredible learning experience, but it's just the beginning.
I didn't have enough time to polish this app or make it so that the information is amazing, this app right now lacks the flair i.e. the reason why I haven't published(deployed) it yet, I would love to keep learning and keep building it.

Some things I'm curious about exploring next are:

* **Real-Time Alerts:** Setting up email or Slack alerts for any new company that gets a "Priority Review" score.  
* **Trend Momentum Tracking:** Instead of just showing what's hot today, visualizing if a trend (like "DePIN") is growing or fading over the last 30 days.  
* **Deeper Founder Analysis:** Integrating data to analyze the track record of the founding team—have they had successful exits before?

Thanks for checking out Project Signal\! I'd love to hear any feedback or ideas.