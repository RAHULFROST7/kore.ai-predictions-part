import pandas as pd
from datetime import datetime, timedelta
import re

class GenerateDate:
    def __init__(self):
        pass

    @staticmethod
    def extract_duration(input_text):
        # Define regex pattern to extract duration in the format 'next (one|<number>) <time_period>'
        regex = r'next\s+(one|two|three|four|five|six|seven|eight|nine|ten|\d+)?\s?(month|quarter|year|season|holiday season|week|spring|summer|fall|winter|festive season|Christmas|Thanksgiving|New Year|summer vacation|rainy season|dry season|monsoon|peak season|off-peak season|high season|low season|peak time)'
        match = re.match(regex, input_text, re.IGNORECASE)
        if match:
            num_str = match.group(1)
            if num_str is None:
                num = 1  # Default to 1 if no number is specified
            elif num_str in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]:
                num = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"].index(num_str) + 1
            else:
                num = int(num_str)
            time_period = match.group(2).lower()
            return num, time_period
        return None, None

    def generate_date_df(self, input_text):
        num, time_period = self.extract_duration(input_text)
        if num is not None and time_period is not None:
            date_range_df = self.generate_date_range(time_period, num)
            return date_range_df
        else:
            # Assume one month by default if input cannot be matched
            date_range_df = self.generate_date_range("month")
            return date_range_df

    @staticmethod
    def generate_next_month_date_range():
        # Get the current date
        current_date = datetime.now()

        # Calculate the first day of the next month
        next_month_start = current_date.replace(day=1) + pd.offsets.DateOffset(months=1)

        # Calculate the last day of the next month
        next_month_end = next_month_start + pd.offsets.MonthEnd(0)

        # Generate the date range for the entire next month
        date_range = pd.date_range(start=next_month_start, end=next_month_end, freq="D")

        # Create the DataFrame with the date range
        df = pd.DataFrame({"Date": date_range})
        df["Day"] = df["Date"].dt.day
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        df = df.drop(["Date"], axis=1)
        return df

    def generate_date_range(self, time_period, duration=1):
        # Get the current date
        current_date = datetime.now()

        if time_period == "month":
            if duration == 1:
                return self.generate_next_month_date_range()
            else:
                # Calculate the first day of the next N months
                start_date = current_date.replace(day=1) + pd.offsets.DateOffset(months=1)

                # Calculate the last day of the Nth month from the start date
                end_date = (start_date + pd.DateOffset(months=duration) - timedelta(days=1))

        elif time_period == "quarter":
            # Calculate the first day of the next quarter
            quarter_number = (current_date.month - 1) // 3 + 2
            start_date = datetime(current_date.year, quarter_number * 3 - 2, 1)

            # Calculate the last day of the next quarter
            end_date = datetime(current_date.year, quarter_number * 3, 1) + pd.DateOffset(months=3) - timedelta(days=1)

        elif time_period == "year":
            if duration == 1:
                # Calculate the first day of the next year
                start_date = datetime(current_date.year + 1, 1, 1)

                # Calculate the last day of the next year
                end_date = datetime(current_date.year + 1, 12, 31)
            else:
                # Calculate the first day of the next N years
                start_date = datetime(current_date.year + 1, 1, 1)

                # Calculate the last day of the Nth year from the start date
                end_date = (start_date + pd.DateOffset(years=duration) - timedelta(days=1))

        elif time_period == "summer":
            # Determine the next summer's year
            next_summer_year = current_date.year if current_date.month <= 6 else current_date.year + 1

            # Calculate the start and end dates of the next summer
            start_date = datetime(next_summer_year, 2, 1)
            end_date = datetime(next_summer_year, 6, 30)

            # Generate the date range for the next summer
            date_range = pd.date_range(start=start_date, end=end_date, freq="D")

            # Create a DataFrame with the date range
            df = pd.DataFrame({"Date": date_range})
            df["Day"] = df["Date"].dt.day
            df["Month"] = df["Date"].dt.month
            df["Year"] = df["Date"].dt.year
            df = df.drop(["Date"], axis=1)
            return df

        elif time_period == "week":
            # Calculate the start and end dates of the next week
            start_date = current_date + pd.DateOffset(weeks=duration - 1)
            end_date = current_date + pd.DateOffset(weeks=duration) - pd.DateOffset(days=1)

        elif time_period == "spring":
            # Determine the next spring's year
            next_spring_year = current_date.year if current_date.month <= 3 else current_date.year + 1

            # Calculate the start and end dates of the next spring
            start_date = datetime(next_spring_year, 3, 1)
            end_date = datetime(next_spring_year, 5, 31)

        elif time_period == "holiday season":
            # Determine the next holiday season's year
            next_holiday_season_year = current_date.year + 1 if current_date.month >= 7 else current_date.year

            # Calculate the start and end dates of the next holiday season
            start_date = datetime(next_holiday_season_year, 4, 15)
            end_date = datetime(next_holiday_season_year, 6, 15) - pd.DateOffset(days=1)

        elif time_period == "christmas":
            # Determine the next Christmas's year
            next_christmas_year = current_date.year if current_date.month <= 12 else current_date.year + 1

            # Calculate the start and end dates of the next Christmas
            start_date = datetime(next_christmas_year, 12, 1)
            end_date = datetime(next_christmas_year, 12, 31)

        else:
            # For unknown time periods, return None for start_date and end_date
            start_date = None
            end_date = None

        if start_date is not None and end_date is not None:
            # Generate the date range
            date_range = pd.date_range(start=start_date, end=end_date, freq="D")

            # Create a DataFrame with the date range
            df = pd.DataFrame({"Date": date_range})
            df["Day"] = df["Date"].dt.day
            df["Month"] = df["Date"].dt.month
            df["Year"] = df["Date"].dt.year
            df = df.drop(["Date"], axis=1)
            return df

        return None