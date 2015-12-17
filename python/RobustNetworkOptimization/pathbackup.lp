Minimize
  Backup_Capacity[0,1] + Backup_Capacity[0,2] + Backup_Capacity[1,0]
   + Backup_Capacity[1,2] + Backup_Capacity[2,0] + Backup_Capacity[2,1]
Subject To
 [CONST]Link_Cap[0][1]: Backup_Capacity[0,1] - 0.025 Backup_Path[0]
   - 0.025 Backup_Path[2] - 0.025 Backup_Path[10] - 2.326347874 U[0,1]
   >= 0
 [CONST]Link_Cap[0][2]: Backup_Capacity[0,2] - 0.025 Backup_Path[1]
   - 0.025 Backup_Path[3] - 0.025 Backup_Path[6] - 2.326347874 U[0,2] >= 0
 [CONST]Link_Cap[1][0]: Backup_Capacity[1,0] - 0.025 Backup_Path[4]
   - 0.025 Backup_Path[6] - 0.025 Backup_Path[9] - 2.326347874 U[1,0] >= 0
 [CONST]Link_Cap[1][2]: Backup_Capacity[1,2] - 0.025 Backup_Path[2]
   - 0.025 Backup_Path[5] - 0.025 Backup_Path[7] - 2.326347874 U[1,2] >= 0
 [CONST]Link_Cap[2][0]: Backup_Capacity[2,0] - 0.025 Backup_Path[5]
   - 0.025 Backup_Path[8] - 0.025 Backup_Path[10] - 2.326347874 U[2,0]
   >= 0
 [CONST]Link_Cap[2][1]: Backup_Capacity[2,1] - 0.025 Backup_Path[1]
   - 0.025 Backup_Path[9] - 0.025 Backup_Path[11] - 2.326347874 U[2,1]
   >= 0
 [CONST]SCOP2[0][1][0][1]: 0.15612494995996 Backup_Path[0] - R[0,1,0,1]
   = 0
 [CONST]SCOP2[0][1][0][2]: 0.15612494995996 Backup_Path[2] - R[0,1,0,2]
   = 0
 [CONST]SCOP2[0][1][1][0]: - R[0,1,1,0] = 0
 [CONST]SCOP2[0][1][1][2]: - R[0,1,1,2] = 0
 [CONST]SCOP2[0][1][2][0]: - R[0,1,2,0] = 0
 [CONST]SCOP2[0][1][2][1]: 0.15612494995996 Backup_Path[10] - R[0,1,2,1]
   = 0
 [CONST]SCOP2[0][2][0][1]: 0.15612494995996 Backup_Path[1] - R[0,2,0,1]
   = 0
 [CONST]SCOP2[0][2][0][2]: 0.15612494995996 Backup_Path[3] - R[0,2,0,2]
   = 0
 [CONST]SCOP2[0][2][1][0]: - R[0,2,1,0] = 0
 [CONST]SCOP2[0][2][1][2]: 0.15612494995996 Backup_Path[6] - R[0,2,1,2]
   = 0
 [CONST]SCOP2[0][2][2][0]: - R[0,2,2,0] = 0
 [CONST]SCOP2[0][2][2][1]: - R[0,2,2,1] = 0
 [CONST]SCOP2[1][0][0][1]: - R[1,0,0,1] = 0
 [CONST]SCOP2[1][0][0][2]: - R[1,0,0,2] = 0
 [CONST]SCOP2[1][0][1][0]: 0.15612494995996 Backup_Path[4] - R[1,0,1,0]
   = 0
 [CONST]SCOP2[1][0][1][2]: 0.15612494995996 Backup_Path[6] - R[1,0,1,2]
   = 0
 [CONST]SCOP2[1][0][2][0]: 0.15612494995996 Backup_Path[9] - R[1,0,2,0]
   = 0
 [CONST]SCOP2[1][0][2][1]: - R[1,0,2,1] = 0
 [CONST]SCOP2[1][2][0][1]: - R[1,2,0,1] = 0
 [CONST]SCOP2[1][2][0][2]: 0.15612494995996 Backup_Path[2] - R[1,2,0,2]
   = 0
 [CONST]SCOP2[1][2][1][0]: 0.15612494995996 Backup_Path[5] - R[1,2,1,0]
   = 0
 [CONST]SCOP2[1][2][1][2]: 0.15612494995996 Backup_Path[7] - R[1,2,1,2]
   = 0
 [CONST]SCOP2[1][2][2][0]: - R[1,2,2,0] = 0
 [CONST]SCOP2[1][2][2][1]: - R[1,2,2,1] = 0
 [CONST]SCOP2[2][0][0][1]: - R[2,0,0,1] = 0
 [CONST]SCOP2[2][0][0][2]: - R[2,0,0,2] = 0
 [CONST]SCOP2[2][0][1][0]: 0.15612494995996 Backup_Path[5] - R[2,0,1,0]
   = 0
 [CONST]SCOP2[2][0][1][2]: - R[2,0,1,2] = 0
 [CONST]SCOP2[2][0][2][0]: 0.15612494995996 Backup_Path[8] - R[2,0,2,0]
   = 0
 [CONST]SCOP2[2][0][2][1]: 0.15612494995996 Backup_Path[10] - R[2,0,2,1]
   = 0
 [CONST]SCOP2[2][1][0][1]: 0.15612494995996 Backup_Path[1] - R[2,1,0,1]
   = 0
 [CONST]SCOP2[2][1][0][2]: - R[2,1,0,2] = 0
 [CONST]SCOP2[2][1][1][0]: - R[2,1,1,0] = 0
 [CONST]SCOP2[2][1][1][2]: - R[2,1,1,2] = 0
 [CONST]SCOP2[2][1][2][0]: 0.15612494995996 Backup_Path[9] - R[2,1,2,0]
   = 0
 [CONST]SCOP2[2][1][2][1]: 0.15612494995996 Backup_Path[11] - R[2,1,2,1]
   = 0
 UniquePath[0,1]: Backup_Path[0] + Backup_Path[1] = 1
 UniquePath[0,2]: Backup_Path[2] + Backup_Path[3] = 1
 UniquePath[1,0]: Backup_Path[4] + Backup_Path[5] = 1
 UniquePath[1,2]: Backup_Path[6] + Backup_Path[7] = 1
 UniquePath[2,0]: Backup_Path[8] + Backup_Path[9] = 1
 UniquePath[2,1]: Backup_Path[10] + Backup_Path[11] = 1
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
 Backup_Path[0] Backup_Path[1] Backup_Path[2] Backup_Path[3] Backup_Path[4]
 Backup_Path[5] Backup_Path[6] Backup_Path[7] Backup_Path[8] Backup_Path[9]
 Backup_Path[10] Backup_Path[11]
End
