from assassins_cred.util.stats_logging import StatsLogger

stats = StatsLogger("../test_resources/stats_log.json")

# data = stats.dataframe
#
# print(data)

stats.stat_lineplot("../test_resources/test.png")
