from models import Camp, Victim
from extensions import db


def compute_analytics():
    """Compute comprehensive analytics for dashboard."""
    total_camps = Camp.query.count()
    total_victims = Victim.query.count()
    
    # Camp statistics
    camp_highest = None
    max_occupancy = 0
    total_capacity = 0
    total_occupancy = 0
    
    for c in Camp.query.all():
        total_capacity += c.max_capacity
        total_occupancy += c.current_occupancy
        if c.current_occupancy > max_occupancy:
            max_occupancy = c.current_occupancy
            camp_highest = c

    # Resource statistics
    food_distributed = Victim.query.filter_by(food_received=True).count()
    medical_distributed = Victim.query.filter_by(medical_kit_received=True).count()
    critical_victims = Victim.query.filter(Victim.health_condition.ilike('critical')).count()
    normal_victims = Victim.query.filter(Victim.health_condition.ilike('normal')).count()
    
    # Camp occupancy details
    camp_details = []
    for c in Camp.query.all():
        camp_details.append({
            'camp_id': c.camp_id,
            'location': c.location,
            'occupancy': c.current_occupancy,
            'capacity': c.max_capacity,
            'occupancy_percentage': c.occupancy_percentage,
            'food_available': c.available_food_packets,
            'medical_available': c.available_medical_kits,
            'volunteers': c.volunteers,
            'status': 'Full' if not c.has_space() else 'Available'
        })
    
    # Victims details
    victim_details = []
    for v in Victim.query.all():
        victim_details.append({
            'victim_id': v.victim_id,
            'name': v.name,
            'age': v.age,
            'health': v.health_condition,
            'camp': v.camp.camp_id if v.camp else 'Unassigned',
            'food_received': 'Yes' if v.food_received else 'No',
            'medical_received': 'Yes' if v.medical_kit_received else 'No'
        })

    return {
        'total_camps': total_camps,
        'total_victims': total_victims,
        'camp_with_highest': camp_highest.camp_id if camp_highest else None,
        'max_occupancy': max_occupancy,
        'total_capacity': total_capacity,
        'total_occupancy': total_occupancy,
        'occupancy_rate': round((total_occupancy / total_capacity * 100), 2) if total_capacity > 0 else 0,
        'food_distributed': food_distributed,
        'medical_distributed': medical_distributed,
        'critical_victims': critical_victims,
        'normal_victims': normal_victims,
        'victims_saved': total_victims - critical_victims,
        'camp_details': camp_details,
        'victim_details': victim_details
    }


def save_analytics_to_file(data, path):
    lines = []
    lines.append(f"Total camps: {data.get('total_camps')}")
    lines.append(f"Total victims: {data.get('total_victims')}")
    lines.append(f"Camp with highest occupancy: {data.get('camp_with_highest')} ({data.get('max_occupancy')})")
    lines.append(f"Total food distributed: {data.get('food_distributed')}")
    lines.append(f"Total medical kits distributed: {data.get('medical_distributed')}")
    lines.append(f"Critical victims: {data.get('critical_victims')}")

    with open(path, 'w') as f:
        f.write('\n'.join(lines))

# TODO: Add more advanced analytics (per camp breakdown, charts, historic trends)
