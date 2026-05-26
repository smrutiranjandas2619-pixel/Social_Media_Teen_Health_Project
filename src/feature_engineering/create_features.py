import numpy as np
import pandas as pd


def create_addiction_score(df):

    if (
        'daily_social_media_hours' in df.columns
        and
        'screen_time_before_sleep' in df.columns
    ):

        df['addiction_score'] = (

            df['daily_social_media_hours']

            *

            df['screen_time_before_sleep']

        )

    return df


def create_sleep_disruption(df):

    if 'sleep_hours' in df.columns:

        df['sleep_disruption'] = np.where(

            df['sleep_hours'] < 6,

            1,

            0

        )

    return df


def create_usage_category(df):

    if 'daily_social_media_hours' in df.columns:

        df['usage_category'] = pd.cut(

            df['daily_social_media_hours'],

            bins=[0,2,5,24],

            labels=[
                'low',
                'medium',
                'high'
            ]

        )

    return df