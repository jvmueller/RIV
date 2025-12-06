import csv
import os
from typing import List
from data.models import Metro
from sqlalchemy.orm import Session



def get_data_file_path(filename: str) -> str:
    basedir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, filename)



def import_metros_from_csv(session: Session, filename: str) -> None:
    full_path = get_data_file_path(filename)

    if not os.path.exists(full_path):
        print(f"CSV file '{full_path}' not found.")
        return

    try:
        with open(full_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            cities_added = cities_skipped = 0
            
            for row in reader:
                try:
                    metro = Metro(
                        name=row['name'].strip(),
                        population=int(row['population'].replace(',', '')),
                        latitude=float(row['latitude']),
                        longitude=float(row['longitude'])
                    )
                    
                    if not session.query(Metro).filter_by(name=metro.name).first():
                        session.add(metro)
                        cities_added += 1
                    else:
                        cities_skipped += 1
                        
                except (ValueError, KeyError) as e:
                    print(f"Skipping row: {row} - Error: {e}")
                    cities_skipped += 1
            
            session.commit()
            print(f"Added {cities_added} metros, skipped {cities_skipped}")
            
    except Exception as e:
        session.rollback()
        print(f"Import error: {e}")



def find_metro(session: Session, metro_name: str, debug: bool = False) -> Metro:
    metro = session.query(Metro).filter(Metro.name.ilike(f'%{metro_name}%')).first()
    if metro:
        if debug:
            print(f"Found metro area: {metro.name}")
        return metro
    else:
        if debug:
            print(f"No metro area found containing '{metro_name}'")
        return None



def clear_metros(session: Session) -> None:
    try:
        deleted = session.query(Metro).delete()
        session.commit()
        print(f"Deleted {deleted} metros")
    except Exception as e:
        session.rollback()
        print(f"Deletion error: {e}")



def get_simplified_name(metro_name: str):
    return metro_name.split('-')[0].strip()
