from assassins_cred.util.stats_logging import StatsLogger
from assassins_cred.constants import resource_file

stats = StatsLogger(f"../{resource_file}/stats_log.json")

# data = stats.dataframe
#
# print(data)

stats.stat_lineplot(f"../{resource_file}/test.png")
