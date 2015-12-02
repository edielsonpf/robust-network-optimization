Minimize
  Backup_Capacity[1,3] + Backup_Capacity[1,2] + Backup_Capacity[1,4]
   + Backup_Capacity[3,1] + Backup_Capacity[3,2] + Backup_Capacity[3,4]
   + Backup_Capacity[2,1] + Backup_Capacity[2,3] + Backup_Capacity[2,4]
   + Backup_Capacity[4,1] + Backup_Capacity[4,3] + Backup_Capacity[4,2]
Subject To
 [CONST]Link_Cap_1_3: Backup_Capacity[1,3] - 0.025 Backup_Link[1,3,1,3]
   - 0.025 Backup_Link[1,3,1,2] - 0.025 Backup_Link[1,3,1,4]
   - 0.025 Backup_Link[1,3,3,1] - 0.025 Backup_Link[1,3,3,2]
   - 0.025 Backup_Link[1,3,3,4] - 0.025 Backup_Link[1,3,2,1]
   - 0.025 Backup_Link[1,3,2,3] - 0.025 Backup_Link[1,3,2,4]
   - 0.025 Backup_Link[1,3,4,1] - 0.025 Backup_Link[1,3,4,3]
   - 0.025 Backup_Link[1,3,4,2] - 2.326347874 U[1,3] >= 0
 [CONST]Link_Cap_1_2: Backup_Capacity[1,2] - 0.025 Backup_Link[1,2,1,3]
   - 0.025 Backup_Link[1,2,1,2] - 0.025 Backup_Link[1,2,1,4]
   - 0.025 Backup_Link[1,2,3,1] - 0.025 Backup_Link[1,2,3,2]
   - 0.025 Backup_Link[1,2,3,4] - 0.025 Backup_Link[1,2,2,1]
   - 0.025 Backup_Link[1,2,2,3] - 0.025 Backup_Link[1,2,2,4]
   - 0.025 Backup_Link[1,2,4,1] - 0.025 Backup_Link[1,2,4,3]
   - 0.025 Backup_Link[1,2,4,2] - 2.326347874 U[1,2] >= 0
 [CONST]Link_Cap_1_4: Backup_Capacity[1,4] - 0.025 Backup_Link[1,4,1,3]
   - 0.025 Backup_Link[1,4,1,2] - 0.025 Backup_Link[1,4,1,4]
   - 0.025 Backup_Link[1,4,3,1] - 0.025 Backup_Link[1,4,3,2]
   - 0.025 Backup_Link[1,4,3,4] - 0.025 Backup_Link[1,4,2,1]
   - 0.025 Backup_Link[1,4,2,3] - 0.025 Backup_Link[1,4,2,4]
   - 0.025 Backup_Link[1,4,4,1] - 0.025 Backup_Link[1,4,4,3]
   - 0.025 Backup_Link[1,4,4,2] - 2.326347874 U[1,4] >= 0
 [CONST]Link_Cap_3_1: Backup_Capacity[3,1] - 0.025 Backup_Link[3,1,1,3]
   - 0.025 Backup_Link[3,1,1,2] - 0.025 Backup_Link[3,1,1,4]
   - 0.025 Backup_Link[3,1,3,1] - 0.025 Backup_Link[3,1,3,2]
   - 0.025 Backup_Link[3,1,3,4] - 0.025 Backup_Link[3,1,2,1]
   - 0.025 Backup_Link[3,1,2,3] - 0.025 Backup_Link[3,1,2,4]
   - 0.025 Backup_Link[3,1,4,1] - 0.025 Backup_Link[3,1,4,3]
   - 0.025 Backup_Link[3,1,4,2] - 2.326347874 U[3,1] >= 0
 [CONST]Link_Cap_3_2: Backup_Capacity[3,2] - 0.025 Backup_Link[3,2,1,3]
   - 0.025 Backup_Link[3,2,1,2] - 0.025 Backup_Link[3,2,1,4]
   - 0.025 Backup_Link[3,2,3,1] - 0.025 Backup_Link[3,2,3,2]
   - 0.025 Backup_Link[3,2,3,4] - 0.025 Backup_Link[3,2,2,1]
   - 0.025 Backup_Link[3,2,2,3] - 0.025 Backup_Link[3,2,2,4]
   - 0.025 Backup_Link[3,2,4,1] - 0.025 Backup_Link[3,2,4,3]
   - 0.025 Backup_Link[3,2,4,2] - 2.326347874 U[3,2] >= 0
 [CONST]Link_Cap_3_4: Backup_Capacity[3,4] - 0.025 Backup_Link[3,4,1,3]
   - 0.025 Backup_Link[3,4,1,2] - 0.025 Backup_Link[3,4,1,4]
   - 0.025 Backup_Link[3,4,3,1] - 0.025 Backup_Link[3,4,3,2]
   - 0.025 Backup_Link[3,4,3,4] - 0.025 Backup_Link[3,4,2,1]
   - 0.025 Backup_Link[3,4,2,3] - 0.025 Backup_Link[3,4,2,4]
   - 0.025 Backup_Link[3,4,4,1] - 0.025 Backup_Link[3,4,4,3]
   - 0.025 Backup_Link[3,4,4,2] - 2.326347874 U[3,4] >= 0
 [CONST]Link_Cap_2_1: Backup_Capacity[2,1] - 0.025 Backup_Link[2,1,1,3]
   - 0.025 Backup_Link[2,1,1,2] - 0.025 Backup_Link[2,1,1,4]
   - 0.025 Backup_Link[2,1,3,1] - 0.025 Backup_Link[2,1,3,2]
   - 0.025 Backup_Link[2,1,3,4] - 0.025 Backup_Link[2,1,2,1]
   - 0.025 Backup_Link[2,1,2,3] - 0.025 Backup_Link[2,1,2,4]
   - 0.025 Backup_Link[2,1,4,1] - 0.025 Backup_Link[2,1,4,3]
   - 0.025 Backup_Link[2,1,4,2] - 2.326347874 U[2,1] >= 0
 [CONST]Link_Cap_2_3: Backup_Capacity[2,3] - 0.025 Backup_Link[2,3,1,3]
   - 0.025 Backup_Link[2,3,1,2] - 0.025 Backup_Link[2,3,1,4]
   - 0.025 Backup_Link[2,3,3,1] - 0.025 Backup_Link[2,3,3,2]
   - 0.025 Backup_Link[2,3,3,4] - 0.025 Backup_Link[2,3,2,1]
   - 0.025 Backup_Link[2,3,2,3] - 0.025 Backup_Link[2,3,2,4]
   - 0.025 Backup_Link[2,3,4,1] - 0.025 Backup_Link[2,3,4,3]
   - 0.025 Backup_Link[2,3,4,2] - 2.326347874 U[2,3] >= 0
 [CONST]Link_Cap_2_4: Backup_Capacity[2,4] - 0.025 Backup_Link[2,4,1,3]
   - 0.025 Backup_Link[2,4,1,2] - 0.025 Backup_Link[2,4,1,4]
   - 0.025 Backup_Link[2,4,3,1] - 0.025 Backup_Link[2,4,3,2]
   - 0.025 Backup_Link[2,4,3,4] - 0.025 Backup_Link[2,4,2,1]
   - 0.025 Backup_Link[2,4,2,3] - 0.025 Backup_Link[2,4,2,4]
   - 0.025 Backup_Link[2,4,4,1] - 0.025 Backup_Link[2,4,4,3]
   - 0.025 Backup_Link[2,4,4,2] - 2.326347874 U[2,4] >= 0
 [CONST]Link_Cap_4_1: Backup_Capacity[4,1] - 0.025 Backup_Link[4,1,1,3]
   - 0.025 Backup_Link[4,1,1,2] - 0.025 Backup_Link[4,1,1,4]
   - 0.025 Backup_Link[4,1,3,1] - 0.025 Backup_Link[4,1,3,2]
   - 0.025 Backup_Link[4,1,3,4] - 0.025 Backup_Link[4,1,2,1]
   - 0.025 Backup_Link[4,1,2,3] - 0.025 Backup_Link[4,1,2,4]
   - 0.025 Backup_Link[4,1,4,1] - 0.025 Backup_Link[4,1,4,3]
   - 0.025 Backup_Link[4,1,4,2] - 2.326347874 U[4,1] >= 0
 [CONST]Link_Cap_4_3: Backup_Capacity[4,3] - 0.025 Backup_Link[4,3,1,3]
   - 0.025 Backup_Link[4,3,1,2] - 0.025 Backup_Link[4,3,1,4]
   - 0.025 Backup_Link[4,3,3,1] - 0.025 Backup_Link[4,3,3,2]
   - 0.025 Backup_Link[4,3,3,4] - 0.025 Backup_Link[4,3,2,1]
   - 0.025 Backup_Link[4,3,2,3] - 0.025 Backup_Link[4,3,2,4]
   - 0.025 Backup_Link[4,3,4,1] - 0.025 Backup_Link[4,3,4,3]
   - 0.025 Backup_Link[4,3,4,2] - 2.326347874 U[4,3] >= 0
 [CONST]Link_Cap_4_2: Backup_Capacity[4,2] - 0.025 Backup_Link[4,2,1,3]
   - 0.025 Backup_Link[4,2,1,2] - 0.025 Backup_Link[4,2,1,4]
   - 0.025 Backup_Link[4,2,3,1] - 0.025 Backup_Link[4,2,3,2]
   - 0.025 Backup_Link[4,2,3,4] - 0.025 Backup_Link[4,2,2,1]
   - 0.025 Backup_Link[4,2,2,3] - 0.025 Backup_Link[4,2,2,4]
   - 0.025 Backup_Link[4,2,4,1] - 0.025 Backup_Link[4,2,4,3]
   - 0.025 Backup_Link[4,2,4,2] - 2.326347874 U[4,2] >= 0
 [CONST]SCOP2[1][3][1][3]: 0.15612494995996 Backup_Link[1,3,1,3]
   - R[1,3,1,3] = 0
 [CONST]SCOP2[1][3][1][2]: 0.15612494995996 Backup_Link[1,3,1,2]
   - R[1,3,1,2] = 0
 [CONST]SCOP2[1][3][1][4]: 0.15612494995996 Backup_Link[1,3,1,4]
   - R[1,3,1,4] = 0
 [CONST]SCOP2[1][3][3][1]: 0.15612494995996 Backup_Link[1,3,3,1]
   - R[1,3,3,1] = 0
 [CONST]SCOP2[1][3][3][2]: 0.15612494995996 Backup_Link[1,3,3,2]
   - R[1,3,3,2] = 0
 [CONST]SCOP2[1][3][3][4]: 0.15612494995996 Backup_Link[1,3,3,4]
   - R[1,3,3,4] = 0
 [CONST]SCOP2[1][3][2][1]: 0.15612494995996 Backup_Link[1,3,2,1]
   - R[1,3,2,1] = 0
 [CONST]SCOP2[1][3][2][3]: 0.15612494995996 Backup_Link[1,3,2,3]
   - R[1,3,2,3] = 0
 [CONST]SCOP2[1][3][2][4]: 0.15612494995996 Backup_Link[1,3,2,4]
   - R[1,3,2,4] = 0
 [CONST]SCOP2[1][3][4][1]: 0.15612494995996 Backup_Link[1,3,4,1]
   - R[1,3,4,1] = 0
 [CONST]SCOP2[1][3][4][3]: 0.15612494995996 Backup_Link[1,3,4,3]
   - R[1,3,4,3] = 0
 [CONST]SCOP2[1][3][4][2]: 0.15612494995996 Backup_Link[1,3,4,2]
   - R[1,3,4,2] = 0
 [CONST]SCOP2[1][2][1][3]: 0.15612494995996 Backup_Link[1,2,1,3]
   - R[1,2,1,3] = 0
 [CONST]SCOP2[1][2][1][2]: 0.15612494995996 Backup_Link[1,2,1,2]
   - R[1,2,1,2] = 0
 [CONST]SCOP2[1][2][1][4]: 0.15612494995996 Backup_Link[1,2,1,4]
   - R[1,2,1,4] = 0
 [CONST]SCOP2[1][2][3][1]: 0.15612494995996 Backup_Link[1,2,3,1]
   - R[1,2,3,1] = 0
 [CONST]SCOP2[1][2][3][2]: 0.15612494995996 Backup_Link[1,2,3,2]
   - R[1,2,3,2] = 0
 [CONST]SCOP2[1][2][3][4]: 0.15612494995996 Backup_Link[1,2,3,4]
   - R[1,2,3,4] = 0
 [CONST]SCOP2[1][2][2][1]: 0.15612494995996 Backup_Link[1,2,2,1]
   - R[1,2,2,1] = 0
 [CONST]SCOP2[1][2][2][3]: 0.15612494995996 Backup_Link[1,2,2,3]
   - R[1,2,2,3] = 0
 [CONST]SCOP2[1][2][2][4]: 0.15612494995996 Backup_Link[1,2,2,4]
   - R[1,2,2,4] = 0
 [CONST]SCOP2[1][2][4][1]: 0.15612494995996 Backup_Link[1,2,4,1]
   - R[1,2,4,1] = 0
 [CONST]SCOP2[1][2][4][3]: 0.15612494995996 Backup_Link[1,2,4,3]
   - R[1,2,4,3] = 0
 [CONST]SCOP2[1][2][4][2]: 0.15612494995996 Backup_Link[1,2,4,2]
   - R[1,2,4,2] = 0
 [CONST]SCOP2[1][4][1][3]: 0.15612494995996 Backup_Link[1,4,1,3]
   - R[1,4,1,3] = 0
 [CONST]SCOP2[1][4][1][2]: 0.15612494995996 Backup_Link[1,4,1,2]
   - R[1,4,1,2] = 0
 [CONST]SCOP2[1][4][1][4]: 0.15612494995996 Backup_Link[1,4,1,4]
   - R[1,4,1,4] = 0
 [CONST]SCOP2[1][4][3][1]: 0.15612494995996 Backup_Link[1,4,3,1]
   - R[1,4,3,1] = 0
 [CONST]SCOP2[1][4][3][2]: 0.15612494995996 Backup_Link[1,4,3,2]
   - R[1,4,3,2] = 0
 [CONST]SCOP2[1][4][3][4]: 0.15612494995996 Backup_Link[1,4,3,4]
   - R[1,4,3,4] = 0
 [CONST]SCOP2[1][4][2][1]: 0.15612494995996 Backup_Link[1,4,2,1]
   - R[1,4,2,1] = 0
 [CONST]SCOP2[1][4][2][3]: 0.15612494995996 Backup_Link[1,4,2,3]
   - R[1,4,2,3] = 0
 [CONST]SCOP2[1][4][2][4]: 0.15612494995996 Backup_Link[1,4,2,4]
   - R[1,4,2,4] = 0
 [CONST]SCOP2[1][4][4][1]: 0.15612494995996 Backup_Link[1,4,4,1]
   - R[1,4,4,1] = 0
 [CONST]SCOP2[1][4][4][3]: 0.15612494995996 Backup_Link[1,4,4,3]
   - R[1,4,4,3] = 0
 [CONST]SCOP2[1][4][4][2]: 0.15612494995996 Backup_Link[1,4,4,2]
   - R[1,4,4,2] = 0
 [CONST]SCOP2[3][1][1][3]: 0.15612494995996 Backup_Link[3,1,1,3]
   - R[3,1,1,3] = 0
 [CONST]SCOP2[3][1][1][2]: 0.15612494995996 Backup_Link[3,1,1,2]
   - R[3,1,1,2] = 0
 [CONST]SCOP2[3][1][1][4]: 0.15612494995996 Backup_Link[3,1,1,4]
   - R[3,1,1,4] = 0
 [CONST]SCOP2[3][1][3][1]: 0.15612494995996 Backup_Link[3,1,3,1]
   - R[3,1,3,1] = 0
 [CONST]SCOP2[3][1][3][2]: 0.15612494995996 Backup_Link[3,1,3,2]
   - R[3,1,3,2] = 0
 [CONST]SCOP2[3][1][3][4]: 0.15612494995996 Backup_Link[3,1,3,4]
   - R[3,1,3,4] = 0
 [CONST]SCOP2[3][1][2][1]: 0.15612494995996 Backup_Link[3,1,2,1]
   - R[3,1,2,1] = 0
 [CONST]SCOP2[3][1][2][3]: 0.15612494995996 Backup_Link[3,1,2,3]
   - R[3,1,2,3] = 0
 [CONST]SCOP2[3][1][2][4]: 0.15612494995996 Backup_Link[3,1,2,4]
   - R[3,1,2,4] = 0
 [CONST]SCOP2[3][1][4][1]: 0.15612494995996 Backup_Link[3,1,4,1]
   - R[3,1,4,1] = 0
 [CONST]SCOP2[3][1][4][3]: 0.15612494995996 Backup_Link[3,1,4,3]
   - R[3,1,4,3] = 0
 [CONST]SCOP2[3][1][4][2]: 0.15612494995996 Backup_Link[3,1,4,2]
   - R[3,1,4,2] = 0
 [CONST]SCOP2[3][2][1][3]: 0.15612494995996 Backup_Link[3,2,1,3]
   - R[3,2,1,3] = 0
 [CONST]SCOP2[3][2][1][2]: 0.15612494995996 Backup_Link[3,2,1,2]
   - R[3,2,1,2] = 0
 [CONST]SCOP2[3][2][1][4]: 0.15612494995996 Backup_Link[3,2,1,4]
   - R[3,2,1,4] = 0
 [CONST]SCOP2[3][2][3][1]: 0.15612494995996 Backup_Link[3,2,3,1]
   - R[3,2,3,1] = 0
 [CONST]SCOP2[3][2][3][2]: 0.15612494995996 Backup_Link[3,2,3,2]
   - R[3,2,3,2] = 0
 [CONST]SCOP2[3][2][3][4]: 0.15612494995996 Backup_Link[3,2,3,4]
   - R[3,2,3,4] = 0
 [CONST]SCOP2[3][2][2][1]: 0.15612494995996 Backup_Link[3,2,2,1]
   - R[3,2,2,1] = 0
 [CONST]SCOP2[3][2][2][3]: 0.15612494995996 Backup_Link[3,2,2,3]
   - R[3,2,2,3] = 0
 [CONST]SCOP2[3][2][2][4]: 0.15612494995996 Backup_Link[3,2,2,4]
   - R[3,2,2,4] = 0
 [CONST]SCOP2[3][2][4][1]: 0.15612494995996 Backup_Link[3,2,4,1]
   - R[3,2,4,1] = 0
 [CONST]SCOP2[3][2][4][3]: 0.15612494995996 Backup_Link[3,2,4,3]
   - R[3,2,4,3] = 0
 [CONST]SCOP2[3][2][4][2]: 0.15612494995996 Backup_Link[3,2,4,2]
   - R[3,2,4,2] = 0
 [CONST]SCOP2[3][4][1][3]: 0.15612494995996 Backup_Link[3,4,1,3]
   - R[3,4,1,3] = 0
 [CONST]SCOP2[3][4][1][2]: 0.15612494995996 Backup_Link[3,4,1,2]
   - R[3,4,1,2] = 0
 [CONST]SCOP2[3][4][1][4]: 0.15612494995996 Backup_Link[3,4,1,4]
   - R[3,4,1,4] = 0
 [CONST]SCOP2[3][4][3][1]: 0.15612494995996 Backup_Link[3,4,3,1]
   - R[3,4,3,1] = 0
 [CONST]SCOP2[3][4][3][2]: 0.15612494995996 Backup_Link[3,4,3,2]
   - R[3,4,3,2] = 0
 [CONST]SCOP2[3][4][3][4]: 0.15612494995996 Backup_Link[3,4,3,4]
   - R[3,4,3,4] = 0
 [CONST]SCOP2[3][4][2][1]: 0.15612494995996 Backup_Link[3,4,2,1]
   - R[3,4,2,1] = 0
 [CONST]SCOP2[3][4][2][3]: 0.15612494995996 Backup_Link[3,4,2,3]
   - R[3,4,2,3] = 0
 [CONST]SCOP2[3][4][2][4]: 0.15612494995996 Backup_Link[3,4,2,4]
   - R[3,4,2,4] = 0
 [CONST]SCOP2[3][4][4][1]: 0.15612494995996 Backup_Link[3,4,4,1]
   - R[3,4,4,1] = 0
 [CONST]SCOP2[3][4][4][3]: 0.15612494995996 Backup_Link[3,4,4,3]
   - R[3,4,4,3] = 0
 [CONST]SCOP2[3][4][4][2]: 0.15612494995996 Backup_Link[3,4,4,2]
   - R[3,4,4,2] = 0
 [CONST]SCOP2[2][1][1][3]: 0.15612494995996 Backup_Link[2,1,1,3]
   - R[2,1,1,3] = 0
 [CONST]SCOP2[2][1][1][2]: 0.15612494995996 Backup_Link[2,1,1,2]
   - R[2,1,1,2] = 0
 [CONST]SCOP2[2][1][1][4]: 0.15612494995996 Backup_Link[2,1,1,4]
   - R[2,1,1,4] = 0
 [CONST]SCOP2[2][1][3][1]: 0.15612494995996 Backup_Link[2,1,3,1]
   - R[2,1,3,1] = 0
 [CONST]SCOP2[2][1][3][2]: 0.15612494995996 Backup_Link[2,1,3,2]
   - R[2,1,3,2] = 0
 [CONST]SCOP2[2][1][3][4]: 0.15612494995996 Backup_Link[2,1,3,4]
   - R[2,1,3,4] = 0
 [CONST]SCOP2[2][1][2][1]: 0.15612494995996 Backup_Link[2,1,2,1]
   - R[2,1,2,1] = 0
 [CONST]SCOP2[2][1][2][3]: 0.15612494995996 Backup_Link[2,1,2,3]
   - R[2,1,2,3] = 0
 [CONST]SCOP2[2][1][2][4]: 0.15612494995996 Backup_Link[2,1,2,4]
   - R[2,1,2,4] = 0
 [CONST]SCOP2[2][1][4][1]: 0.15612494995996 Backup_Link[2,1,4,1]
   - R[2,1,4,1] = 0
 [CONST]SCOP2[2][1][4][3]: 0.15612494995996 Backup_Link[2,1,4,3]
   - R[2,1,4,3] = 0
 [CONST]SCOP2[2][1][4][2]: 0.15612494995996 Backup_Link[2,1,4,2]
   - R[2,1,4,2] = 0
 [CONST]SCOP2[2][3][1][3]: 0.15612494995996 Backup_Link[2,3,1,3]
   - R[2,3,1,3] = 0
 [CONST]SCOP2[2][3][1][2]: 0.15612494995996 Backup_Link[2,3,1,2]
   - R[2,3,1,2] = 0
 [CONST]SCOP2[2][3][1][4]: 0.15612494995996 Backup_Link[2,3,1,4]
   - R[2,3,1,4] = 0
 [CONST]SCOP2[2][3][3][1]: 0.15612494995996 Backup_Link[2,3,3,1]
   - R[2,3,3,1] = 0
 [CONST]SCOP2[2][3][3][2]: 0.15612494995996 Backup_Link[2,3,3,2]
   - R[2,3,3,2] = 0
 [CONST]SCOP2[2][3][3][4]: 0.15612494995996 Backup_Link[2,3,3,4]
   - R[2,3,3,4] = 0
 [CONST]SCOP2[2][3][2][1]: 0.15612494995996 Backup_Link[2,3,2,1]
   - R[2,3,2,1] = 0
 [CONST]SCOP2[2][3][2][3]: 0.15612494995996 Backup_Link[2,3,2,3]
   - R[2,3,2,3] = 0
 [CONST]SCOP2[2][3][2][4]: 0.15612494995996 Backup_Link[2,3,2,4]
   - R[2,3,2,4] = 0
 [CONST]SCOP2[2][3][4][1]: 0.15612494995996 Backup_Link[2,3,4,1]
   - R[2,3,4,1] = 0
 [CONST]SCOP2[2][3][4][3]: 0.15612494995996 Backup_Link[2,3,4,3]
   - R[2,3,4,3] = 0
 [CONST]SCOP2[2][3][4][2]: 0.15612494995996 Backup_Link[2,3,4,2]
   - R[2,3,4,2] = 0
 [CONST]SCOP2[2][4][1][3]: 0.15612494995996 Backup_Link[2,4,1,3]
   - R[2,4,1,3] = 0
 [CONST]SCOP2[2][4][1][2]: 0.15612494995996 Backup_Link[2,4,1,2]
   - R[2,4,1,2] = 0
 [CONST]SCOP2[2][4][1][4]: 0.15612494995996 Backup_Link[2,4,1,4]
   - R[2,4,1,4] = 0
 [CONST]SCOP2[2][4][3][1]: 0.15612494995996 Backup_Link[2,4,3,1]
   - R[2,4,3,1] = 0
 [CONST]SCOP2[2][4][3][2]: 0.15612494995996 Backup_Link[2,4,3,2]
   - R[2,4,3,2] = 0
 [CONST]SCOP2[2][4][3][4]: 0.15612494995996 Backup_Link[2,4,3,4]
   - R[2,4,3,4] = 0
 [CONST]SCOP2[2][4][2][1]: 0.15612494995996 Backup_Link[2,4,2,1]
   - R[2,4,2,1] = 0
 [CONST]SCOP2[2][4][2][3]: 0.15612494995996 Backup_Link[2,4,2,3]
   - R[2,4,2,3] = 0
 [CONST]SCOP2[2][4][2][4]: 0.15612494995996 Backup_Link[2,4,2,4]
   - R[2,4,2,4] = 0
 [CONST]SCOP2[2][4][4][1]: 0.15612494995996 Backup_Link[2,4,4,1]
   - R[2,4,4,1] = 0
 [CONST]SCOP2[2][4][4][3]: 0.15612494995996 Backup_Link[2,4,4,3]
   - R[2,4,4,3] = 0
 [CONST]SCOP2[2][4][4][2]: 0.15612494995996 Backup_Link[2,4,4,2]
   - R[2,4,4,2] = 0
 [CONST]SCOP2[4][1][1][3]: 0.15612494995996 Backup_Link[4,1,1,3]
   - R[4,1,1,3] = 0
 [CONST]SCOP2[4][1][1][2]: 0.15612494995996 Backup_Link[4,1,1,2]
   - R[4,1,1,2] = 0
 [CONST]SCOP2[4][1][1][4]: 0.15612494995996 Backup_Link[4,1,1,4]
   - R[4,1,1,4] = 0
 [CONST]SCOP2[4][1][3][1]: 0.15612494995996 Backup_Link[4,1,3,1]
   - R[4,1,3,1] = 0
 [CONST]SCOP2[4][1][3][2]: 0.15612494995996 Backup_Link[4,1,3,2]
   - R[4,1,3,2] = 0
 [CONST]SCOP2[4][1][3][4]: 0.15612494995996 Backup_Link[4,1,3,4]
   - R[4,1,3,4] = 0
 [CONST]SCOP2[4][1][2][1]: 0.15612494995996 Backup_Link[4,1,2,1]
   - R[4,1,2,1] = 0
 [CONST]SCOP2[4][1][2][3]: 0.15612494995996 Backup_Link[4,1,2,3]
   - R[4,1,2,3] = 0
 [CONST]SCOP2[4][1][2][4]: 0.15612494995996 Backup_Link[4,1,2,4]
   - R[4,1,2,4] = 0
 [CONST]SCOP2[4][1][4][1]: 0.15612494995996 Backup_Link[4,1,4,1]
   - R[4,1,4,1] = 0
 [CONST]SCOP2[4][1][4][3]: 0.15612494995996 Backup_Link[4,1,4,3]
   - R[4,1,4,3] = 0
 [CONST]SCOP2[4][1][4][2]: 0.15612494995996 Backup_Link[4,1,4,2]
   - R[4,1,4,2] = 0
 [CONST]SCOP2[4][3][1][3]: 0.15612494995996 Backup_Link[4,3,1,3]
   - R[4,3,1,3] = 0
 [CONST]SCOP2[4][3][1][2]: 0.15612494995996 Backup_Link[4,3,1,2]
   - R[4,3,1,2] = 0
 [CONST]SCOP2[4][3][1][4]: 0.15612494995996 Backup_Link[4,3,1,4]
   - R[4,3,1,4] = 0
 [CONST]SCOP2[4][3][3][1]: 0.15612494995996 Backup_Link[4,3,3,1]
   - R[4,3,3,1] = 0
 [CONST]SCOP2[4][3][3][2]: 0.15612494995996 Backup_Link[4,3,3,2]
   - R[4,3,3,2] = 0
 [CONST]SCOP2[4][3][3][4]: 0.15612494995996 Backup_Link[4,3,3,4]
   - R[4,3,3,4] = 0
 [CONST]SCOP2[4][3][2][1]: 0.15612494995996 Backup_Link[4,3,2,1]
   - R[4,3,2,1] = 0
 [CONST]SCOP2[4][3][2][3]: 0.15612494995996 Backup_Link[4,3,2,3]
   - R[4,3,2,3] = 0
 [CONST]SCOP2[4][3][2][4]: 0.15612494995996 Backup_Link[4,3,2,4]
   - R[4,3,2,4] = 0
 [CONST]SCOP2[4][3][4][1]: 0.15612494995996 Backup_Link[4,3,4,1]
   - R[4,3,4,1] = 0
 [CONST]SCOP2[4][3][4][3]: 0.15612494995996 Backup_Link[4,3,4,3]
   - R[4,3,4,3] = 0
 [CONST]SCOP2[4][3][4][2]: 0.15612494995996 Backup_Link[4,3,4,2]
   - R[4,3,4,2] = 0
 [CONST]SCOP2[4][2][1][3]: 0.15612494995996 Backup_Link[4,2,1,3]
   - R[4,2,1,3] = 0
 [CONST]SCOP2[4][2][1][2]: 0.15612494995996 Backup_Link[4,2,1,2]
   - R[4,2,1,2] = 0
 [CONST]SCOP2[4][2][1][4]: 0.15612494995996 Backup_Link[4,2,1,4]
   - R[4,2,1,4] = 0
 [CONST]SCOP2[4][2][3][1]: 0.15612494995996 Backup_Link[4,2,3,1]
   - R[4,2,3,1] = 0
 [CONST]SCOP2[4][2][3][2]: 0.15612494995996 Backup_Link[4,2,3,2]
   - R[4,2,3,2] = 0
 [CONST]SCOP2[4][2][3][4]: 0.15612494995996 Backup_Link[4,2,3,4]
   - R[4,2,3,4] = 0
 [CONST]SCOP2[4][2][2][1]: 0.15612494995996 Backup_Link[4,2,2,1]
   - R[4,2,2,1] = 0
 [CONST]SCOP2[4][2][2][3]: 0.15612494995996 Backup_Link[4,2,2,3]
   - R[4,2,2,3] = 0
 [CONST]SCOP2[4][2][2][4]: 0.15612494995996 Backup_Link[4,2,2,4]
   - R[4,2,2,4] = 0
 [CONST]SCOP2[4][2][4][1]: 0.15612494995996 Backup_Link[4,2,4,1]
   - R[4,2,4,1] = 0
 [CONST]SCOP2[4][2][4][3]: 0.15612494995996 Backup_Link[4,2,4,3]
   - R[4,2,4,3] = 0
 [CONST]SCOP2[4][2][4][2]: 0.15612494995996 Backup_Link[4,2,4,2]
   - R[4,2,4,2] = 0
 Flow1[1,2,1,3]: Backup_Link[1,3,1,3] + Backup_Link[1,2,1,3]
   + Backup_Link[1,4,1,3] - Backup_Link[3,1,1,3] - Backup_Link[2,1,1,3]
   - Backup_Link[4,1,1,3] = 1
 Flow1[1,2,1,2]: Backup_Link[1,3,1,2] + Backup_Link[1,2,1,2]
   + Backup_Link[1,4,1,2] - Backup_Link[3,1,1,2] - Backup_Link[2,1,1,2]
   - Backup_Link[4,1,1,2] = 1
 Flow1[1,2,1,4]: Backup_Link[1,3,1,4] + Backup_Link[1,2,1,4]
   + Backup_Link[1,4,1,4] - Backup_Link[3,1,1,4] - Backup_Link[2,1,1,4]
   - Backup_Link[4,1,1,4] = 1
 Flow2[1,2,3,1]: Backup_Link[1,3,3,1] + Backup_Link[1,2,3,1]
   + Backup_Link[1,4,3,1] - Backup_Link[3,1,3,1] - Backup_Link[2,1,3,1]
   - Backup_Link[4,1,3,1] = -1
 Flow3[1,2,3,2]: Backup_Link[1,3,3,2] + Backup_Link[1,2,3,2]
   + Backup_Link[1,4,3,2] - Backup_Link[3,1,3,2] - Backup_Link[2,1,3,2]
   - Backup_Link[4,1,3,2] = 0
 Flow3[1,2,3,4]: Backup_Link[1,3,3,4] + Backup_Link[1,2,3,4]
   + Backup_Link[1,4,3,4] - Backup_Link[3,1,3,4] - Backup_Link[2,1,3,4]
   - Backup_Link[4,1,3,4] = 0
 Flow2[1,2,2,1]: Backup_Link[1,3,2,1] + Backup_Link[1,2,2,1]
   + Backup_Link[1,4,2,1] - Backup_Link[3,1,2,1] - Backup_Link[2,1,2,1]
   - Backup_Link[4,1,2,1] = -1
 Flow3[1,2,2,3]: Backup_Link[1,3,2,3] + Backup_Link[1,2,2,3]
   + Backup_Link[1,4,2,3] - Backup_Link[3,1,2,3] - Backup_Link[2,1,2,3]
   - Backup_Link[4,1,2,3] = 0
 Flow3[1,2,2,4]: Backup_Link[1,3,2,4] + Backup_Link[1,2,2,4]
   + Backup_Link[1,4,2,4] - Backup_Link[3,1,2,4] - Backup_Link[2,1,2,4]
   - Backup_Link[4,1,2,4] = 0
 Flow2[1,2,4,1]: Backup_Link[1,3,4,1] + Backup_Link[1,2,4,1]
   + Backup_Link[1,4,4,1] - Backup_Link[3,1,4,1] - Backup_Link[2,1,4,1]
   - Backup_Link[4,1,4,1] = -1
 Flow3[1,2,4,3]: Backup_Link[1,3,4,3] + Backup_Link[1,2,4,3]
   + Backup_Link[1,4,4,3] - Backup_Link[3,1,4,3] - Backup_Link[2,1,4,3]
   - Backup_Link[4,1,4,3] = 0
 Flow3[1,2,4,2]: Backup_Link[1,3,4,2] + Backup_Link[1,2,4,2]
   + Backup_Link[1,4,4,2] - Backup_Link[3,1,4,2] - Backup_Link[2,1,4,2]
   - Backup_Link[4,1,4,2] = 0
 Flow2[3,2,1,3]: - Backup_Link[1,3,1,3] + Backup_Link[3,1,1,3]
   + Backup_Link[3,2,1,3] + Backup_Link[3,4,1,3] - Backup_Link[2,3,1,3]
   - Backup_Link[4,3,1,3] = -1
 Flow3[3,2,1,2]: - Backup_Link[1,3,1,2] + Backup_Link[3,1,1,2]
   + Backup_Link[3,2,1,2] + Backup_Link[3,4,1,2] - Backup_Link[2,3,1,2]
   - Backup_Link[4,3,1,2] = 0
 Flow3[3,2,1,4]: - Backup_Link[1,3,1,4] + Backup_Link[3,1,1,4]
   + Backup_Link[3,2,1,4] + Backup_Link[3,4,1,4] - Backup_Link[2,3,1,4]
   - Backup_Link[4,3,1,4] = 0
 Flow1[3,2,3,1]: - Backup_Link[1,3,3,1] + Backup_Link[3,1,3,1]
   + Backup_Link[3,2,3,1] + Backup_Link[3,4,3,1] - Backup_Link[2,3,3,1]
   - Backup_Link[4,3,3,1] = 1
 Flow1[3,2,3,2]: - Backup_Link[1,3,3,2] + Backup_Link[3,1,3,2]
   + Backup_Link[3,2,3,2] + Backup_Link[3,4,3,2] - Backup_Link[2,3,3,2]
   - Backup_Link[4,3,3,2] = 1
 Flow1[3,2,3,4]: - Backup_Link[1,3,3,4] + Backup_Link[3,1,3,4]
   + Backup_Link[3,2,3,4] + Backup_Link[3,4,3,4] - Backup_Link[2,3,3,4]
   - Backup_Link[4,3,3,4] = 1
 Flow3[3,2,2,1]: - Backup_Link[1,3,2,1] + Backup_Link[3,1,2,1]
   + Backup_Link[3,2,2,1] + Backup_Link[3,4,2,1] - Backup_Link[2,3,2,1]
   - Backup_Link[4,3,2,1] = 0
 Flow2[3,2,2,3]: - Backup_Link[1,3,2,3] + Backup_Link[3,1,2,3]
   + Backup_Link[3,2,2,3] + Backup_Link[3,4,2,3] - Backup_Link[2,3,2,3]
   - Backup_Link[4,3,2,3] = -1
 Flow3[3,2,2,4]: - Backup_Link[1,3,2,4] + Backup_Link[3,1,2,4]
   + Backup_Link[3,2,2,4] + Backup_Link[3,4,2,4] - Backup_Link[2,3,2,4]
   - Backup_Link[4,3,2,4] = 0
 Flow3[3,2,4,1]: - Backup_Link[1,3,4,1] + Backup_Link[3,1,4,1]
   + Backup_Link[3,2,4,1] + Backup_Link[3,4,4,1] - Backup_Link[2,3,4,1]
   - Backup_Link[4,3,4,1] = 0
 Flow2[3,2,4,3]: - Backup_Link[1,3,4,3] + Backup_Link[3,1,4,3]
   + Backup_Link[3,2,4,3] + Backup_Link[3,4,4,3] - Backup_Link[2,3,4,3]
   - Backup_Link[4,3,4,3] = -1
 Flow3[3,2,4,2]: - Backup_Link[1,3,4,2] + Backup_Link[3,1,4,2]
   + Backup_Link[3,2,4,2] + Backup_Link[3,4,4,2] - Backup_Link[2,3,4,2]
   - Backup_Link[4,3,4,2] = 0
 Flow3[2,2,1,3]: - Backup_Link[1,2,1,3] - Backup_Link[3,2,1,3]
   + Backup_Link[2,1,1,3] + Backup_Link[2,3,1,3] + Backup_Link[2,4,1,3]
   - Backup_Link[4,2,1,3] = 0
 Flow2[2,2,1,2]: - Backup_Link[1,2,1,2] - Backup_Link[3,2,1,2]
   + Backup_Link[2,1,1,2] + Backup_Link[2,3,1,2] + Backup_Link[2,4,1,2]
   - Backup_Link[4,2,1,2] = -1
 Flow3[2,2,1,4]: - Backup_Link[1,2,1,4] - Backup_Link[3,2,1,4]
   + Backup_Link[2,1,1,4] + Backup_Link[2,3,1,4] + Backup_Link[2,4,1,4]
   - Backup_Link[4,2,1,4] = 0
 Flow3[2,2,3,1]: - Backup_Link[1,2,3,1] - Backup_Link[3,2,3,1]
   + Backup_Link[2,1,3,1] + Backup_Link[2,3,3,1] + Backup_Link[2,4,3,1]
   - Backup_Link[4,2,3,1] = 0
 Flow2[2,2,3,2]: - Backup_Link[1,2,3,2] - Backup_Link[3,2,3,2]
   + Backup_Link[2,1,3,2] + Backup_Link[2,3,3,2] + Backup_Link[2,4,3,2]
   - Backup_Link[4,2,3,2] = -1
 Flow3[2,2,3,4]: - Backup_Link[1,2,3,4] - Backup_Link[3,2,3,4]
   + Backup_Link[2,1,3,4] + Backup_Link[2,3,3,4] + Backup_Link[2,4,3,4]
   - Backup_Link[4,2,3,4] = 0
 Flow1[2,2,2,1]: - Backup_Link[1,2,2,1] - Backup_Link[3,2,2,1]
   + Backup_Link[2,1,2,1] + Backup_Link[2,3,2,1] + Backup_Link[2,4,2,1]
   - Backup_Link[4,2,2,1] = 1
 Flow1[2,2,2,3]: - Backup_Link[1,2,2,3] - Backup_Link[3,2,2,3]
   + Backup_Link[2,1,2,3] + Backup_Link[2,3,2,3] + Backup_Link[2,4,2,3]
   - Backup_Link[4,2,2,3] = 1
 Flow1[2,2,2,4]: - Backup_Link[1,2,2,4] - Backup_Link[3,2,2,4]
   + Backup_Link[2,1,2,4] + Backup_Link[2,3,2,4] + Backup_Link[2,4,2,4]
   - Backup_Link[4,2,2,4] = 1
 Flow3[2,2,4,1]: - Backup_Link[1,2,4,1] - Backup_Link[3,2,4,1]
   + Backup_Link[2,1,4,1] + Backup_Link[2,3,4,1] + Backup_Link[2,4,4,1]
   - Backup_Link[4,2,4,1] = 0
 Flow3[2,2,4,3]: - Backup_Link[1,2,4,3] - Backup_Link[3,2,4,3]
   + Backup_Link[2,1,4,3] + Backup_Link[2,3,4,3] + Backup_Link[2,4,4,3]
   - Backup_Link[4,2,4,3] = 0
 Flow2[2,2,4,2]: - Backup_Link[1,2,4,2] - Backup_Link[3,2,4,2]
   + Backup_Link[2,1,4,2] + Backup_Link[2,3,4,2] + Backup_Link[2,4,4,2]
   - Backup_Link[4,2,4,2] = -1
 Flow3[4,2,1,3]: - Backup_Link[1,4,1,3] - Backup_Link[3,4,1,3]
   - Backup_Link[2,4,1,3] + Backup_Link[4,1,1,3] + Backup_Link[4,3,1,3]
   + Backup_Link[4,2,1,3] = 0
 Flow3[4,2,1,2]: - Backup_Link[1,4,1,2] - Backup_Link[3,4,1,2]
   - Backup_Link[2,4,1,2] + Backup_Link[4,1,1,2] + Backup_Link[4,3,1,2]
   + Backup_Link[4,2,1,2] = 0
 Flow2[4,2,1,4]: - Backup_Link[1,4,1,4] - Backup_Link[3,4,1,4]
   - Backup_Link[2,4,1,4] + Backup_Link[4,1,1,4] + Backup_Link[4,3,1,4]
   + Backup_Link[4,2,1,4] = -1
 Flow3[4,2,3,1]: - Backup_Link[1,4,3,1] - Backup_Link[3,4,3,1]
   - Backup_Link[2,4,3,1] + Backup_Link[4,1,3,1] + Backup_Link[4,3,3,1]
   + Backup_Link[4,2,3,1] = 0
 Flow3[4,2,3,2]: - Backup_Link[1,4,3,2] - Backup_Link[3,4,3,2]
   - Backup_Link[2,4,3,2] + Backup_Link[4,1,3,2] + Backup_Link[4,3,3,2]
   + Backup_Link[4,2,3,2] = 0
 Flow2[4,2,3,4]: - Backup_Link[1,4,3,4] - Backup_Link[3,4,3,4]
   - Backup_Link[2,4,3,4] + Backup_Link[4,1,3,4] + Backup_Link[4,3,3,4]
   + Backup_Link[4,2,3,4] = -1
 Flow3[4,2,2,1]: - Backup_Link[1,4,2,1] - Backup_Link[3,4,2,1]
   - Backup_Link[2,4,2,1] + Backup_Link[4,1,2,1] + Backup_Link[4,3,2,1]
   + Backup_Link[4,2,2,1] = 0
 Flow3[4,2,2,3]: - Backup_Link[1,4,2,3] - Backup_Link[3,4,2,3]
   - Backup_Link[2,4,2,3] + Backup_Link[4,1,2,3] + Backup_Link[4,3,2,3]
   + Backup_Link[4,2,2,3] = 0
 Flow2[4,2,2,4]: - Backup_Link[1,4,2,4] - Backup_Link[3,4,2,4]
   - Backup_Link[2,4,2,4] + Backup_Link[4,1,2,4] + Backup_Link[4,3,2,4]
   + Backup_Link[4,2,2,4] = -1
 Flow1[4,2,4,1]: - Backup_Link[1,4,4,1] - Backup_Link[3,4,4,1]
   - Backup_Link[2,4,4,1] + Backup_Link[4,1,4,1] + Backup_Link[4,3,4,1]
   + Backup_Link[4,2,4,1] = 1
 Flow1[4,2,4,3]: - Backup_Link[1,4,4,3] - Backup_Link[3,4,4,3]
   - Backup_Link[2,4,4,3] + Backup_Link[4,1,4,3] + Backup_Link[4,3,4,3]
   + Backup_Link[4,2,4,3] = 1
 Flow1[4,2,4,2]: - Backup_Link[1,4,4,2] - Backup_Link[3,4,4,2]
   - Backup_Link[2,4,4,2] + Backup_Link[4,1,4,2] + Backup_Link[4,3,4,2]
   + Backup_Link[4,2,4,2] = 1
 [CONST]SCOP1[1][3]: [ - U[1,3] ^2 + R[1,3,1,3] ^2 + R[1,3,1,2] ^2
   + R[1,3,1,4] ^2 + R[1,3,3,1] ^2 + R[1,3,3,2] ^2 + R[1,3,3,4] ^2
   + R[1,3,2,1] ^2 + R[1,3,2,3] ^2 + R[1,3,2,4] ^2 + R[1,3,4,1] ^2
   + R[1,3,4,3] ^2 + R[1,3,4,2] ^2 ] <= 0
 [CONST]SCOP1[1][2]: [ - U[1,2] ^2 + R[1,2,1,3] ^2 + R[1,2,1,2] ^2
   + R[1,2,1,4] ^2 + R[1,2,3,1] ^2 + R[1,2,3,2] ^2 + R[1,2,3,4] ^2
   + R[1,2,2,1] ^2 + R[1,2,2,3] ^2 + R[1,2,2,4] ^2 + R[1,2,4,1] ^2
   + R[1,2,4,3] ^2 + R[1,2,4,2] ^2 ] <= 0
 [CONST]SCOP1[1][4]: [ - U[1,4] ^2 + R[1,4,1,3] ^2 + R[1,4,1,2] ^2
   + R[1,4,1,4] ^2 + R[1,4,3,1] ^2 + R[1,4,3,2] ^2 + R[1,4,3,4] ^2
   + R[1,4,2,1] ^2 + R[1,4,2,3] ^2 + R[1,4,2,4] ^2 + R[1,4,4,1] ^2
   + R[1,4,4,3] ^2 + R[1,4,4,2] ^2 ] <= 0
 [CONST]SCOP1[3][1]: [ - U[3,1] ^2 + R[3,1,1,3] ^2 + R[3,1,1,2] ^2
   + R[3,1,1,4] ^2 + R[3,1,3,1] ^2 + R[3,1,3,2] ^2 + R[3,1,3,4] ^2
   + R[3,1,2,1] ^2 + R[3,1,2,3] ^2 + R[3,1,2,4] ^2 + R[3,1,4,1] ^2
   + R[3,1,4,3] ^2 + R[3,1,4,2] ^2 ] <= 0
 [CONST]SCOP1[3][2]: [ - U[3,2] ^2 + R[3,2,1,3] ^2 + R[3,2,1,2] ^2
   + R[3,2,1,4] ^2 + R[3,2,3,1] ^2 + R[3,2,3,2] ^2 + R[3,2,3,4] ^2
   + R[3,2,2,1] ^2 + R[3,2,2,3] ^2 + R[3,2,2,4] ^2 + R[3,2,4,1] ^2
   + R[3,2,4,3] ^2 + R[3,2,4,2] ^2 ] <= 0
 [CONST]SCOP1[3][4]: [ - U[3,4] ^2 + R[3,4,1,3] ^2 + R[3,4,1,2] ^2
   + R[3,4,1,4] ^2 + R[3,4,3,1] ^2 + R[3,4,3,2] ^2 + R[3,4,3,4] ^2
   + R[3,4,2,1] ^2 + R[3,4,2,3] ^2 + R[3,4,2,4] ^2 + R[3,4,4,1] ^2
   + R[3,4,4,3] ^2 + R[3,4,4,2] ^2 ] <= 0
 [CONST]SCOP1[2][1]: [ - U[2,1] ^2 + R[2,1,1,3] ^2 + R[2,1,1,2] ^2
   + R[2,1,1,4] ^2 + R[2,1,3,1] ^2 + R[2,1,3,2] ^2 + R[2,1,3,4] ^2
   + R[2,1,2,1] ^2 + R[2,1,2,3] ^2 + R[2,1,2,4] ^2 + R[2,1,4,1] ^2
   + R[2,1,4,3] ^2 + R[2,1,4,2] ^2 ] <= 0
 [CONST]SCOP1[2][3]: [ - U[2,3] ^2 + R[2,3,1,3] ^2 + R[2,3,1,2] ^2
   + R[2,3,1,4] ^2 + R[2,3,3,1] ^2 + R[2,3,3,2] ^2 + R[2,3,3,4] ^2
   + R[2,3,2,1] ^2 + R[2,3,2,3] ^2 + R[2,3,2,4] ^2 + R[2,3,4,1] ^2
   + R[2,3,4,3] ^2 + R[2,3,4,2] ^2 ] <= 0
 [CONST]SCOP1[2][4]: [ - U[2,4] ^2 + R[2,4,1,3] ^2 + R[2,4,1,2] ^2
   + R[2,4,1,4] ^2 + R[2,4,3,1] ^2 + R[2,4,3,2] ^2 + R[2,4,3,4] ^2
   + R[2,4,2,1] ^2 + R[2,4,2,3] ^2 + R[2,4,2,4] ^2 + R[2,4,4,1] ^2
   + R[2,4,4,3] ^2 + R[2,4,4,2] ^2 ] <= 0
 [CONST]SCOP1[4][1]: [ - U[4,1] ^2 + R[4,1,1,3] ^2 + R[4,1,1,2] ^2
   + R[4,1,1,4] ^2 + R[4,1,3,1] ^2 + R[4,1,3,2] ^2 + R[4,1,3,4] ^2
   + R[4,1,2,1] ^2 + R[4,1,2,3] ^2 + R[4,1,2,4] ^2 + R[4,1,4,1] ^2
   + R[4,1,4,3] ^2 + R[4,1,4,2] ^2 ] <= 0
 [CONST]SCOP1[4][3]: [ - U[4,3] ^2 + R[4,3,1,3] ^2 + R[4,3,1,2] ^2
   + R[4,3,1,4] ^2 + R[4,3,3,1] ^2 + R[4,3,3,2] ^2 + R[4,3,3,4] ^2
   + R[4,3,2,1] ^2 + R[4,3,2,3] ^2 + R[4,3,2,4] ^2 + R[4,3,4,1] ^2
   + R[4,3,4,3] ^2 + R[4,3,4,2] ^2 ] <= 0
 [CONST]SCOP1[4][2]: [ - U[4,2] ^2 + R[4,2,1,3] ^2 + R[4,2,1,2] ^2
   + R[4,2,1,4] ^2 + R[4,2,3,1] ^2 + R[4,2,3,2] ^2 + R[4,2,3,4] ^2
   + R[4,2,2,1] ^2 + R[4,2,2,3] ^2 + R[4,2,2,4] ^2 + R[4,2,4,1] ^2
   + R[4,2,4,3] ^2 + R[4,2,4,2] ^2 ] <= 0
Bounds
Binaries
 Backup_Link[1,3,1,3] Backup_Link[1,3,1,2] Backup_Link[1,3,1,4]
 Backup_Link[1,3,3,1] Backup_Link[1,3,3,2] Backup_Link[1,3,3,4]
 Backup_Link[1,3,2,1] Backup_Link[1,3,2,3] Backup_Link[1,3,2,4]
 Backup_Link[1,3,4,1] Backup_Link[1,3,4,3] Backup_Link[1,3,4,2]
 Backup_Link[1,2,1,3] Backup_Link[1,2,1,2] Backup_Link[1,2,1,4]
 Backup_Link[1,2,3,1] Backup_Link[1,2,3,2] Backup_Link[1,2,3,4]
 Backup_Link[1,2,2,1] Backup_Link[1,2,2,3] Backup_Link[1,2,2,4]
 Backup_Link[1,2,4,1] Backup_Link[1,2,4,3] Backup_Link[1,2,4,2]
 Backup_Link[1,4,1,3] Backup_Link[1,4,1,2] Backup_Link[1,4,1,4]
 Backup_Link[1,4,3,1] Backup_Link[1,4,3,2] Backup_Link[1,4,3,4]
 Backup_Link[1,4,2,1] Backup_Link[1,4,2,3] Backup_Link[1,4,2,4]
 Backup_Link[1,4,4,1] Backup_Link[1,4,4,3] Backup_Link[1,4,4,2]
 Backup_Link[3,1,1,3] Backup_Link[3,1,1,2] Backup_Link[3,1,1,4]
 Backup_Link[3,1,3,1] Backup_Link[3,1,3,2] Backup_Link[3,1,3,4]
 Backup_Link[3,1,2,1] Backup_Link[3,1,2,3] Backup_Link[3,1,2,4]
 Backup_Link[3,1,4,1] Backup_Link[3,1,4,3] Backup_Link[3,1,4,2]
 Backup_Link[3,2,1,3] Backup_Link[3,2,1,2] Backup_Link[3,2,1,4]
 Backup_Link[3,2,3,1] Backup_Link[3,2,3,2] Backup_Link[3,2,3,4]
 Backup_Link[3,2,2,1] Backup_Link[3,2,2,3] Backup_Link[3,2,2,4]
 Backup_Link[3,2,4,1] Backup_Link[3,2,4,3] Backup_Link[3,2,4,2]
 Backup_Link[3,4,1,3] Backup_Link[3,4,1,2] Backup_Link[3,4,1,4]
 Backup_Link[3,4,3,1] Backup_Link[3,4,3,2] Backup_Link[3,4,3,4]
 Backup_Link[3,4,2,1] Backup_Link[3,4,2,3] Backup_Link[3,4,2,4]
 Backup_Link[3,4,4,1] Backup_Link[3,4,4,3] Backup_Link[3,4,4,2]
 Backup_Link[2,1,1,3] Backup_Link[2,1,1,2] Backup_Link[2,1,1,4]
 Backup_Link[2,1,3,1] Backup_Link[2,1,3,2] Backup_Link[2,1,3,4]
 Backup_Link[2,1,2,1] Backup_Link[2,1,2,3] Backup_Link[2,1,2,4]
 Backup_Link[2,1,4,1] Backup_Link[2,1,4,3] Backup_Link[2,1,4,2]
 Backup_Link[2,3,1,3] Backup_Link[2,3,1,2] Backup_Link[2,3,1,4]
 Backup_Link[2,3,3,1] Backup_Link[2,3,3,2] Backup_Link[2,3,3,4]
 Backup_Link[2,3,2,1] Backup_Link[2,3,2,3] Backup_Link[2,3,2,4]
 Backup_Link[2,3,4,1] Backup_Link[2,3,4,3] Backup_Link[2,3,4,2]
 Backup_Link[2,4,1,3] Backup_Link[2,4,1,2] Backup_Link[2,4,1,4]
 Backup_Link[2,4,3,1] Backup_Link[2,4,3,2] Backup_Link[2,4,3,4]
 Backup_Link[2,4,2,1] Backup_Link[2,4,2,3] Backup_Link[2,4,2,4]
 Backup_Link[2,4,4,1] Backup_Link[2,4,4,3] Backup_Link[2,4,4,2]
 Backup_Link[4,1,1,3] Backup_Link[4,1,1,2] Backup_Link[4,1,1,4]
 Backup_Link[4,1,3,1] Backup_Link[4,1,3,2] Backup_Link[4,1,3,4]
 Backup_Link[4,1,2,1] Backup_Link[4,1,2,3] Backup_Link[4,1,2,4]
 Backup_Link[4,1,4,1] Backup_Link[4,1,4,3] Backup_Link[4,1,4,2]
 Backup_Link[4,3,1,3] Backup_Link[4,3,1,2] Backup_Link[4,3,1,4]
 Backup_Link[4,3,3,1] Backup_Link[4,3,3,2] Backup_Link[4,3,3,4]
 Backup_Link[4,3,2,1] Backup_Link[4,3,2,3] Backup_Link[4,3,2,4]
 Backup_Link[4,3,4,1] Backup_Link[4,3,4,3] Backup_Link[4,3,4,2]
 Backup_Link[4,2,1,3] Backup_Link[4,2,1,2] Backup_Link[4,2,1,4]
 Backup_Link[4,2,3,1] Backup_Link[4,2,3,2] Backup_Link[4,2,3,4]
 Backup_Link[4,2,2,1] Backup_Link[4,2,2,3] Backup_Link[4,2,2,4]
 Backup_Link[4,2,4,1] Backup_Link[4,2,4,3] Backup_Link[4,2,4,2]
End
