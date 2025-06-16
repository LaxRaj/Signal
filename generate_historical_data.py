# generate_historical_data.py
import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_data(num_records=500):
    """Generates a realistic, simulated historical dataset of startup news."""
    data = []
    start_date = pd.to_datetime("2023-06-01")
    
    for _ in range(num_records):
        company_name = fake.company().replace(',', '')
        date = start_date + pd.to_timedelta(np.random.randint(0, 730), 'd')
        source = random.choice(['TechCrunch', 'Product Hunt'])
        
        # Increased probability of funding events to make data more interesting
        event_type = random.choices(['funding', 'launch'], weights=[0.5, 0.5], k=1)[0]
        
        outcome = "N/A"
        roi_potential = 0

        if event_type == 'funding':
            series = random.choice(['Seed', 'Series A', 'Series B'])
            amount = random.randint(1, 50)
            title = f"{company_name} raises ${amount}M in {series} funding"
            description = f"The company, operating in the {fake.bs()} space, secured funding to expand its team."
            # Increased probability of a defined outcome
            if random.random() < 0.6: # 60% chance of a positive outcome
                outcome = f"Acquired for ${amount * random.randint(5, 20)}M"
                roi_potential = float(outcome.split('$')[1].split('M')[0]) / amount
            elif random.random() < 0.2: # 20% chance of failure
                outcome = "Shut down"
                roi_potential = -1
        elif event_type == 'launch':
            title = f"{company_name} launches new platform for {fake.bs()}"
            description = f"A new product launch from {company_name} aims to disrupt the market."
            if random.random() < 0.5: # 50% chance of a good outcome post-launch
                series = random.choice(['Seed', 'Series A'])
                outcome = f"Raised {series} funding 12 months post-launch"
                roi_potential = random.uniform(2, 5)
        else:
            title = f"{company_name} announces partnership with {fake.company()}"
            description = "General tech news update."

        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'source': source,
            'title': title,
            'description': description,
            'company_name': company_name,
            'outcome': outcome,
            'roi_potential': roi_potential
        })
        
    df = pd.DataFrame(data)
    df.to_csv('historical_data.csv', index=False)
    print(f"Generated historical_data.csv with {len(df)} records.")

if __name__ == "__main__":
    generate_data() 