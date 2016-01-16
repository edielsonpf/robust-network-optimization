Minimize
  Backup_Capacity[0,1] + Backup_Capacity[0,2] + Backup_Capacity[1,0]
   + Backup_Capacity[1,2] + Backup_Capacity[2,0] + Backup_Capacity[2,1]
Subject To
 [CONST]Link_Cap_0_1: Backup_Capacity[0,1] - 0.05 Backup_Link[0,1,0,1]
   - 0.025 Backup_Link[0,1,0,2] - 0.05 Backup_Link[0,1,1,0]
   - 0.025 Backup_Link[0,1,1,2] - 0.05 Backup_Link[0,1,2,0]
   - 0.025 Backup_Link[0,1,2,1] - 2.326347874 U[0,1] >= 0
 [CONST]Link_Cap_0_2: Backup_Capacity[0,2] - 0.05 Backup_Link[0,2,0,1]
   - 0.025 Backup_Link[0,2,0,2] - 0.05 Backup_Link[0,2,1,0]
   - 0.025 Backup_Link[0,2,1,2] - 0.05 Backup_Link[0,2,2,0]
   - 0.025 Backup_Link[0,2,2,1] - 2.326347874 U[0,2] >= 0
 [CONST]Link_Cap_1_0: Backup_Capacity[1,0] - 0.05 Backup_Link[1,0,0,1]
   - 0.025 Backup_Link[1,0,0,2] - 0.05 Backup_Link[1,0,1,0]
   - 0.025 Backup_Link[1,0,1,2] - 0.05 Backup_Link[1,0,2,0]
   - 0.025 Backup_Link[1,0,2,1] - 2.326347874 U[1,0] >= 0
 [CONST]Link_Cap_1_2: Backup_Capacity[1,2] - 0.05 Backup_Link[1,2,0,1]
   - 0.025 Backup_Link[1,2,0,2] - 0.05 Backup_Link[1,2,1,0]
   - 0.025 Backup_Link[1,2,1,2] - 0.05 Backup_Link[1,2,2,0]
   - 0.025 Backup_Link[1,2,2,1] - 2.326347874 U[1,2] >= 0
 [CONST]Link_Cap_2_0: Backup_Capacity[2,0] - 0.05 Backup_Link[2,0,0,1]
   - 0.025 Backup_Link[2,0,0,2] - 0.05 Backup_Link[2,0,1,0]
   - 0.025 Backup_Link[2,0,1,2] - 0.05 Backup_Link[2,0,2,0]
   - 0.025 Backup_Link[2,0,2,1] - 2.326347874 U[2,0] >= 0
 [CONST]Link_Cap_2_1: Backup_Capacity[2,1] - 0.05 Backup_Link[2,1,0,1]
   - 0.025 Backup_Link[2,1,0,2] - 0.05 Backup_Link[2,1,1,0]
   - 0.025 Backup_Link[2,1,1,2] - 0.05 Backup_Link[2,1,2,0]
   - 0.025 Backup_Link[2,1,2,1] - 2.326347874 U[2,1] >= 0
 [CONST]SCOP2[0][1][0][1]: 0.2179449471770337 Backup_Link[0,1,0,1]
   - R[0,1,0,1] = 0
 [CONST]SCOP2[0][1][0][2]: 0.15612494995996 Backup_Link[0,1,0,2]
   - R[0,1,0,2] = 0
 [CONST]SCOP2[0][1][1][0]: 0.2179449471770337 Backup_Link[0,1,1,0]
   - R[0,1,1,0] = 0
 [CONST]SCOP2[0][1][1][2]: 0.15612494995996 Backup_Link[0,1,1,2]
   - R[0,1,1,2] = 0
 [CONST]SCOP2[0][1][2][0]: 0.2179449471770337 Backup_Link[0,1,2,0]
   - R[0,1,2,0] = 0
 [CONST]SCOP2[0][1][2][1]: 0.15612494995996 Backup_Link[0,1,2,1]
   - R[0,1,2,1] = 0
 [CONST]SCOP2[0][2][0][1]: 0.2179449471770337 Backup_Link[0,2,0,1]
   - R[0,2,0,1] = 0
 [CONST]SCOP2[0][2][0][2]: 0.15612494995996 Backup_Link[0,2,0,2]
   - R[0,2,0,2] = 0
 [CONST]SCOP2[0][2][1][0]: 0.2179449471770337 Backup_Link[0,2,1,0]
   - R[0,2,1,0] = 0
 [CONST]SCOP2[0][2][1][2]: 0.15612494995996 Backup_Link[0,2,1,2]
   - R[0,2,1,2] = 0
 [CONST]SCOP2[0][2][2][0]: 0.2179449471770337 Backup_Link[0,2,2,0]
   - R[0,2,2,0] = 0
 [CONST]SCOP2[0][2][2][1]: 0.15612494995996 Backup_Link[0,2,2,1]
   - R[0,2,2,1] = 0
 [CONST]SCOP2[1][0][0][1]: 0.2179449471770337 Backup_Link[1,0,0,1]
   - R[1,0,0,1] = 0
 [CONST]SCOP2[1][0][0][2]: 0.15612494995996 Backup_Link[1,0,0,2]
   - R[1,0,0,2] = 0
 [CONST]SCOP2[1][0][1][0]: 0.2179449471770337 Backup_Link[1,0,1,0]
   - R[1,0,1,0] = 0
 [CONST]SCOP2[1][0][1][2]: 0.15612494995996 Backup_Link[1,0,1,2]
   - R[1,0,1,2] = 0
 [CONST]SCOP2[1][0][2][0]: 0.2179449471770337 Backup_Link[1,0,2,0]
   - R[1,0,2,0] = 0
 [CONST]SCOP2[1][0][2][1]: 0.15612494995996 Backup_Link[1,0,2,1]
   - R[1,0,2,1] = 0
 [CONST]SCOP2[1][2][0][1]: 0.2179449471770337 Backup_Link[1,2,0,1]
   - R[1,2,0,1] = 0
 [CONST]SCOP2[1][2][0][2]: 0.15612494995996 Backup_Link[1,2,0,2]
   - R[1,2,0,2] = 0
 [CONST]SCOP2[1][2][1][0]: 0.2179449471770337 Backup_Link[1,2,1,0]
   - R[1,2,1,0] = 0
 [CONST]SCOP2[1][2][1][2]: 0.15612494995996 Backup_Link[1,2,1,2]
   - R[1,2,1,2] = 0
 [CONST]SCOP2[1][2][2][0]: 0.2179449471770337 Backup_Link[1,2,2,0]
   - R[1,2,2,0] = 0
 [CONST]SCOP2[1][2][2][1]: 0.15612494995996 Backup_Link[1,2,2,1]
   - R[1,2,2,1] = 0
 [CONST]SCOP2[2][0][0][1]: 0.2179449471770337 Backup_Link[2,0,0,1]
   - R[2,0,0,1] = 0
 [CONST]SCOP2[2][0][0][2]: 0.15612494995996 Backup_Link[2,0,0,2]
   - R[2,0,0,2] = 0
 [CONST]SCOP2[2][0][1][0]: 0.2179449471770337 Backup_Link[2,0,1,0]
   - R[2,0,1,0] = 0
 [CONST]SCOP2[2][0][1][2]: 0.15612494995996 Backup_Link[2,0,1,2]
   - R[2,0,1,2] = 0
 [CONST]SCOP2[2][0][2][0]: 0.2179449471770337 Backup_Link[2,0,2,0]
   - R[2,0,2,0] = 0
 [CONST]SCOP2[2][0][2][1]: 0.15612494995996 Backup_Link[2,0,2,1]
   - R[2,0,2,1] = 0
 [CONST]SCOP2[2][1][0][1]: 0.2179449471770337 Backup_Link[2,1,0,1]
   - R[2,1,0,1] = 0
 [CONST]SCOP2[2][1][0][2]: 0.15612494995996 Backup_Link[2,1,0,2]
   - R[2,1,0,2] = 0
 [CONST]SCOP2[2][1][1][0]: 0.2179449471770337 Backup_Link[2,1,1,0]
   - R[2,1,1,0] = 0
 [CONST]SCOP2[2][1][1][2]: 0.15612494995996 Backup_Link[2,1,1,2]
   - R[2,1,1,2] = 0
 [CONST]SCOP2[2][1][2][0]: 0.2179449471770337 Backup_Link[2,1,2,0]
   - R[2,1,2,0] = 0
 [CONST]SCOP2[2][1][2][1]: 0.15612494995996 Backup_Link[2,1,2,1]
   - R[2,1,2,1] = 0
 Flow1[0,1,0,1]: Backup_Link[0,1,0,1] + Backup_Link[0,2,0,1]
   - Backup_Link[1,0,0,1] - Backup_Link[2,0,0,1] = 1
 Flow1[0,1,0,2]: Backup_Link[0,1,0,2] + Backup_Link[0,2,0,2]
   - Backup_Link[1,0,0,2] - Backup_Link[2,0,0,2] = 1
 Flow2[0,1,1,0]: Backup_Link[0,1,1,0] + Backup_Link[0,2,1,0]
   - Backup_Link[1,0,1,0] - Backup_Link[2,0,1,0] = -1
 Flow3[0,1,1,2]: Backup_Link[0,1,1,2] + Backup_Link[0,2,1,2]
   - Backup_Link[1,0,1,2] - Backup_Link[2,0,1,2] = 0
 Flow2[0,1,2,0]: Backup_Link[0,1,2,0] + Backup_Link[0,2,2,0]
   - Backup_Link[1,0,2,0] - Backup_Link[2,0,2,0] = -1
 Flow3[0,1,2,1]: Backup_Link[0,1,2,1] + Backup_Link[0,2,2,1]
   - Backup_Link[1,0,2,1] - Backup_Link[2,0,2,1] = 0
 Flow2[1,1,0,1]: - Backup_Link[0,1,0,1] + Backup_Link[1,0,0,1]
   + Backup_Link[1,2,0,1] - Backup_Link[2,1,0,1] = -1
 Flow3[1,1,0,2]: - Backup_Link[0,1,0,2] + Backup_Link[1,0,0,2]
   + Backup_Link[1,2,0,2] - Backup_Link[2,1,0,2] = 0
 Flow1[1,1,1,0]: - Backup_Link[0,1,1,0] + Backup_Link[1,0,1,0]
   + Backup_Link[1,2,1,0] - Backup_Link[2,1,1,0] = 1
 Flow1[1,1,1,2]: - Backup_Link[0,1,1,2] + Backup_Link[1,0,1,2]
   + Backup_Link[1,2,1,2] - Backup_Link[2,1,1,2] = 1
 Flow3[1,1,2,0]: - Backup_Link[0,1,2,0] + Backup_Link[1,0,2,0]
   + Backup_Link[1,2,2,0] - Backup_Link[2,1,2,0] = 0
 Flow2[1,1,2,1]: - Backup_Link[0,1,2,1] + Backup_Link[1,0,2,1]
   + Backup_Link[1,2,2,1] - Backup_Link[2,1,2,1] = -1
 Flow3[2,1,0,1]: - Backup_Link[0,2,0,1] - Backup_Link[1,2,0,1]
   + Backup_Link[2,0,0,1] + Backup_Link[2,1,0,1] = 0
 Flow2[2,1,0,2]: - Backup_Link[0,2,0,2] - Backup_Link[1,2,0,2]
   + Backup_Link[2,0,0,2] + Backup_Link[2,1,0,2] = -1
 Flow3[2,1,1,0]: - Backup_Link[0,2,1,0] - Backup_Link[1,2,1,0]
   + Backup_Link[2,0,1,0] + Backup_Link[2,1,1,0] = 0
 Flow2[2,1,1,2]: - Backup_Link[0,2,1,2] - Backup_Link[1,2,1,2]
   + Backup_Link[2,0,1,2] + Backup_Link[2,1,1,2] = -1
 Flow1[2,1,2,0]: - Backup_Link[0,2,2,0] - Backup_Link[1,2,2,0]
   + Backup_Link[2,0,2,0] + Backup_Link[2,1,2,0] = 1
 Flow1[2,1,2,1]: - Backup_Link[0,2,2,1] - Backup_Link[1,2,2,1]
   + Backup_Link[2,0,2,1] + Backup_Link[2,1,2,1] = 1
 [CONST]SCOP1[0][1]: [ - U[0,1] ^2 + R[0,1,0,1] ^2 + R[0,1,0,2] ^2
   + R[0,1,1,0] ^2 + R[0,1,1,2] ^2 + R[0,1,2,0] ^2 + R[0,1,2,1] ^2 ] <= 0
 [CONST]SCOP1[0][2]: [ - U[0,2] ^2 + R[0,2,0,1] ^2 + R[0,2,0,2] ^2
   + R[0,2,1,0] ^2 + R[0,2,1,2] ^2 + R[0,2,2,0] ^2 + R[0,2,2,1] ^2 ] <= 0
 [CONST]SCOP1[1][0]: [ - U[1,0] ^2 + R[1,0,0,1] ^2 + R[1,0,0,2] ^2
   + R[1,0,1,0] ^2 + R[1,0,1,2] ^2 + R[1,0,2,0] ^2 + R[1,0,2,1] ^2 ] <= 0
 [CONST]SCOP1[1][2]: [ - U[1,2] ^2 + R[1,2,0,1] ^2 + R[1,2,0,2] ^2
   + R[1,2,1,0] ^2 + R[1,2,1,2] ^2 + R[1,2,2,0] ^2 + R[1,2,2,1] ^2 ] <= 0
 [CONST]SCOP1[2][0]: [ - U[2,0] ^2 + R[2,0,0,1] ^2 + R[2,0,0,2] ^2
   + R[2,0,1,0] ^2 + R[2,0,1,2] ^2 + R[2,0,2,0] ^2 + R[2,0,2,1] ^2 ] <= 0
 [CONST]SCOP1[2][1]: [ - U[2,1] ^2 + R[2,1,0,1] ^2 + R[2,1,0,2] ^2
   + R[2,1,1,0] ^2 + R[2,1,1,2] ^2 + R[2,1,2,0] ^2 + R[2,1,2,1] ^2 ] <= 0
Bounds
Binaries
 Backup_Link[0,1,0,1] Backup_Link[0,1,0,2] Backup_Link[0,1,1,0]
 Backup_Link[0,1,1,2] Backup_Link[0,1,2,0] Backup_Link[0,1,2,1]
 Backup_Link[0,2,0,1] Backup_Link[0,2,0,2] Backup_Link[0,2,1,0]
 Backup_Link[0,2,1,2] Backup_Link[0,2,2,0] Backup_Link[0,2,2,1]
 Backup_Link[1,0,0,1] Backup_Link[1,0,0,2] Backup_Link[1,0,1,0]
 Backup_Link[1,0,1,2] Backup_Link[1,0,2,0] Backup_Link[1,0,2,1]
 Backup_Link[1,2,0,1] Backup_Link[1,2,0,2] Backup_Link[1,2,1,0]
 Backup_Link[1,2,1,2] Backup_Link[1,2,2,0] Backup_Link[1,2,2,1]
 Backup_Link[2,0,0,1] Backup_Link[2,0,0,2] Backup_Link[2,0,1,0]
 Backup_Link[2,0,1,2] Backup_Link[2,0,2,0] Backup_Link[2,0,2,1]
 Backup_Link[2,1,0,1] Backup_Link[2,1,0,2] Backup_Link[2,1,1,0]
 Backup_Link[2,1,1,2] Backup_Link[2,1,2,0] Backup_Link[2,1,2,1]
End
