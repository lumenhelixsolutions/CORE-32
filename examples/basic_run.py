from core32 import Core32Supervisor

sup = Core32Supervisor(state=0)
sup.execute("P_DELTA32", ctx="example")
sup.execute("P_RHO32", ctx="example")
sup.set_sandbox(True)
sup.execute("P_SWAPPAIR_0", ctx="example")

for record in sup.log.records:
    print(record)
