from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..school import School

import json
import datetime
import typing as t
from .school import students_by_grade

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class StatsLogger:
    def __init__(self, filename: str):
        self.filename = filename
        with open(self.filename) as f:
            self.stats: t.List[t.Dict[str]] = json.load(f)["stats"]

        self.decode_datetimes()

        self._df = None
        self._df_stats = self.stats

    def encode_datetimes(self):
        for stat in self.stats:
            stat["datetime"] = datetime.datetime.strftime(stat["datetime"], DATETIME_FORMAT)

    def decode_datetimes(self):
        for stat in self.stats:
            stat["datetime"] = datetime.datetime.strptime(stat["datetime"], DATETIME_FORMAT)

    def write(self):
        self.encode_datetimes()
        with open(self.filename, "w") as f:
            json.dump({"stats": self.stats}, f, indent=2)

    def add_stat(self, school: School, date: datetime.datetime) -> None:
        self.stats.append({
            "datetime": date,
            "grades": students_by_grade(school)
        })

    def get_grade(self, grade: str) -> t.Dict[datetime.datetime, int]:
        grade_stats = {}
        for stat in self.stats:
            if grade in stat["grades"]:
                grade_stats[stat["datetime"]] = stat["grades"][grade]

        return grade_stats

    @property
    def dataframe(self):
        if self._df is None or self._df_stats != self.stats:
            data = {"grade": [], "datetime": [], "count": []}
            for grade in ["8", "9", "10", "11", "12"]:
                for date, count in self.get_grade(grade).items():
                    data["grade"].append(grade)
                    data["datetime"].append(date)
                    data["count"].append(count)
            self._df = pd.DataFrame(data)
            self._df_stats = self.stats
        return self._df

    def stat_lineplot(self, filename: str):
        data = self.dataframe
        print(data)
        lineplot = sns.lineplot(data=data, x="datetime", y="count", style="grade")
        lineplot.get_figure().savefig(filename, bbox_inches="tight")
        plt.clf()
