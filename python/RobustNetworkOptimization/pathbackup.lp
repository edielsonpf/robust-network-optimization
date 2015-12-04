Minimize
  Backup_Capacity[0,1] + Backup_Capacity[0,2] + Backup_Capacity[0,3]
   + Backup_Capacity[1,0] + Backup_Capacity[1,2] + Backup_Capacity[1,3]
   + Backup_Capacity[2,0] + Backup_Capacity[2,1] + Backup_Capacity[2,3]
   + Backup_Capacity[3,0] + Backup_Capacity[3,1] + Backup_Capacity[3,2]
Subject To
 [CONST]Link_Cap[0][1]: Backup_Capacity[0,1] - 0.025 Backup_Path[0]
   - 0.025 Backup_Path[5] - 0.025 Backup_Path[6] - 0.025 Backup_Path[10]
   - 0.025 Backup_Path[11] - 0.025 Backup_Path[35] - 0.025 Backup_Path[38]
   - 0.025 Backup_Path[40] - 0.025 Backup_Path[50] - 0.025 Backup_Path[53]
   - 0.025 Backup_Path[55] - 2.326347874 U[0,1] >= 0
 [CONST]Link_Cap[0][2]: Backup_Capacity[0,2] - 0.025 Backup_Path[1]
   - 0.025 Backup_Path[2] - 0.025 Backup_Path[7] - 0.025 Backup_Path[12]
   - 0.025 Backup_Path[13] - 0.025 Backup_Path[20] - 0.025 Backup_Path[23]
   - 0.025 Backup_Path[25] - 0.025 Backup_Path[51] - 0.025 Backup_Path[56]
   - 0.025 Backup_Path[57] - 2.326347874 U[0,2] >= 0
 [CONST]Link_Cap[0][3]: Backup_Capacity[0,3] - 0.025 Backup_Path[3]
   - 0.025 Backup_Path[4] - 0.025 Backup_Path[8] - 0.025 Backup_Path[9]
   - 0.025 Backup_Path[14] - 0.025 Backup_Path[21] - 0.025 Backup_Path[26]
   - 0.025 Backup_Path[27] - 0.025 Backup_Path[36] - 0.025 Backup_Path[41]
   - 0.025 Backup_Path[42] - 2.326347874 U[0,3] >= 0
 [CONST]Link_Cap[1][0]: Backup_Capacity[1,0] - 0.025 Backup_Path[15]
   - 0.025 Backup_Path[20] - 0.025 Backup_Path[21] - 0.025 Backup_Path[25]
   - 0.025 Backup_Path[26] - 0.025 Backup_Path[31] - 0.025 Backup_Path[34]
   - 0.025 Backup_Path[42] - 0.025 Backup_Path[46] - 0.025 Backup_Path[49]
   - 0.025 Backup_Path[57] - 2.326347874 U[1,0] >= 0
 [CONST]Link_Cap[1][2]: Backup_Capacity[1,2] - 0.025 Backup_Path[5]
   - 0.025 Backup_Path[8] - 0.025 Backup_Path[10] - 0.025 Backup_Path[16]
   - 0.025 Backup_Path[17] - 0.025 Backup_Path[22] - 0.025 Backup_Path[27]
   - 0.025 Backup_Path[28] - 0.025 Backup_Path[47] - 0.025 Backup_Path[55]
   - 0.025 Backup_Path[58] - 2.326347874 U[1,2] >= 0
 [CONST]Link_Cap[1][3]: Backup_Capacity[1,3] - 0.025 Backup_Path[6]
   - 0.025 Backup_Path[11] - 0.025 Backup_Path[12] - 0.025 Backup_Path[18]
   - 0.025 Backup_Path[19] - 0.025 Backup_Path[23] - 0.025 Backup_Path[24]
   - 0.025 Backup_Path[29] - 0.025 Backup_Path[32] - 0.025 Backup_Path[40]
   - 0.025 Backup_Path[43] - 2.326347874 U[1,3] >= 0
 [CONST]Link_Cap[2][0]: Backup_Capacity[2,0] - 0.025 Backup_Path[16]
   - 0.025 Backup_Path[19] - 0.025 Backup_Path[27] - 0.025 Backup_Path[30]
   - 0.025 Backup_Path[35] - 0.025 Backup_Path[36] - 0.025 Backup_Path[40]
   - 0.025 Backup_Path[41] - 0.025 Backup_Path[47] - 0.025 Backup_Path[48]
   - 0.025 Backup_Path[53] - 2.326347874 U[2,0] >= 0
 [CONST]Link_Cap[2][1]: Backup_Capacity[2,1] - 0.025 Backup_Path[1]
   - 0.025 Backup_Path[4] - 0.025 Backup_Path[12] - 0.025 Backup_Path[31]
   - 0.025 Backup_Path[32] - 0.025 Backup_Path[37] - 0.025 Backup_Path[42]
   - 0.025 Backup_Path[43] - 0.025 Backup_Path[49] - 0.025 Backup_Path[51]
   - 0.025 Backup_Path[54] - 2.326347874 U[2,1] >= 0
 [CONST]Link_Cap[2][3]: Backup_Capacity[2,3] - 0.025 Backup_Path[2]
   - 0.025 Backup_Path[10] - 0.025 Backup_Path[13] - 0.025 Backup_Path[17]
   - 0.025 Backup_Path[25] - 0.025 Backup_Path[28] - 0.025 Backup_Path[33]
   - 0.025 Backup_Path[34] - 0.025 Backup_Path[38] - 0.025 Backup_Path[39]
   - 0.025 Backup_Path[44] - 2.326347874 U[2,3] >= 0
 [CONST]Link_Cap[3][0]: Backup_Capacity[3,0] - 0.025 Backup_Path[17]
   - 0.025 Backup_Path[18] - 0.025 Backup_Path[23] - 0.025 Backup_Path[32]
   - 0.025 Backup_Path[33] - 0.025 Backup_Path[38] - 0.025 Backup_Path[45]
   - 0.025 Backup_Path[50] - 0.025 Backup_Path[51] - 0.025 Backup_Path[55]
   - 0.025 Backup_Path[56] - 2.326347874 U[3,0] >= 0
 [CONST]Link_Cap[3][1]: Backup_Capacity[3,1] - 0.025 Backup_Path[2]
   - 0.025 Backup_Path[3] - 0.025 Backup_Path[8] - 0.025 Backup_Path[34]
   - 0.025 Backup_Path[36] - 0.025 Backup_Path[39] - 0.025 Backup_Path[46]
   - 0.025 Backup_Path[47] - 0.025 Backup_Path[52] - 0.025 Backup_Path[57]
   - 0.025 Backup_Path[58] - 2.326347874 U[3,1] >= 0
 [CONST]Link_Cap[3][2]: Backup_Capacity[3,2] - 0.025 Backup_Path[4]
   - 0.025 Backup_Path[6] - 0.025 Backup_Path[9] - 0.025 Backup_Path[19]
   - 0.025 Backup_Path[21] - 0.025 Backup_Path[24] - 0.025 Backup_Path[48]
   - 0.025 Backup_Path[49] - 0.025 Backup_Path[53] - 0.025 Backup_Path[54]
   - 0.025 Backup_Path[59] - 2.326347874 U[3,2] >= 0
 [CONST]SCOP2[0][1][0][1]: 0.15612494995996 Backup_Path[0] - R[0,1,0,1]
   = 0
 [CONST]SCOP2[0][1][0][2]: 0.15612494995996 Backup_Path[5]
   + 0.15612494995996 Backup_Path[6] - R[0,1,0,2] = 0
 [CONST]SCOP2[0][1][0][3]: 0.15612494995996 Backup_Path[10]
   + 0.15612494995996 Backup_Path[11] - R[0,1,0,3] = 0
 [CONST]SCOP2[0][1][1][0]: - R[0,1,1,0] = 0
 [CONST]SCOP2[0][1][1][2]: - R[0,1,1,2] = 0
 [CONST]SCOP2[0][1][1][3]: - R[0,1,1,3] = 0
 [CONST]SCOP2[0][1][2][0]: - R[0,1,2,0] = 0
 [CONST]SCOP2[0][1][2][1]: 0.15612494995996 Backup_Path[35]
   + 0.15612494995996 Backup_Path[38] - R[0,1,2,1] = 0
 [CONST]SCOP2[0][1][2][3]: 0.15612494995996 Backup_Path[40] - R[0,1,2,3]
   = 0
 [CONST]SCOP2[0][1][3][0]: - R[0,1,3,0] = 0
 [CONST]SCOP2[0][1][3][1]: 0.15612494995996 Backup_Path[50]
   + 0.15612494995996 Backup_Path[53] - R[0,1,3,1] = 0
 [CONST]SCOP2[0][1][3][2]: 0.15612494995996 Backup_Path[55] - R[0,1,3,2]
   = 0
 [CONST]SCOP2[0][2][0][1]: 0.15612494995996 Backup_Path[1]
   + 0.15612494995996 Backup_Path[2] - R[0,2,0,1] = 0
 [CONST]SCOP2[0][2][0][2]: 0.15612494995996 Backup_Path[7] - R[0,2,0,2]
   = 0
 [CONST]SCOP2[0][2][0][3]: 0.15612494995996 Backup_Path[12]
   + 0.15612494995996 Backup_Path[13] - R[0,2,0,3] = 0
 [CONST]SCOP2[0][2][1][0]: - R[0,2,1,0] = 0
 [CONST]SCOP2[0][2][1][2]: 0.15612494995996 Backup_Path[20]
   + 0.15612494995996 Backup_Path[23] - R[0,2,1,2] = 0
 [CONST]SCOP2[0][2][1][3]: 0.15612494995996 Backup_Path[25] - R[0,2,1,3]
   = 0
 [CONST]SCOP2[0][2][2][0]: - R[0,2,2,0] = 0
 [CONST]SCOP2[0][2][2][1]: - R[0,2,2,1] = 0
 [CONST]SCOP2[0][2][2][3]: - R[0,2,2,3] = 0
 [CONST]SCOP2[0][2][3][0]: - R[0,2,3,0] = 0
 [CONST]SCOP2[0][2][3][1]: 0.15612494995996 Backup_Path[51] - R[0,2,3,1]
   = 0
 [CONST]SCOP2[0][2][3][2]: 0.15612494995996 Backup_Path[56]
   + 0.15612494995996 Backup_Path[57] - R[0,2,3,2] = 0
 [CONST]SCOP2[0][3][0][1]: 0.15612494995996 Backup_Path[3]
   + 0.15612494995996 Backup_Path[4] - R[0,3,0,1] = 0
 [CONST]SCOP2[0][3][0][2]: 0.15612494995996 Backup_Path[8]
   + 0.15612494995996 Backup_Path[9] - R[0,3,0,2] = 0
 [CONST]SCOP2[0][3][0][3]: 0.15612494995996 Backup_Path[14] - R[0,3,0,3]
   = 0
 [CONST]SCOP2[0][3][1][0]: - R[0,3,1,0] = 0
 [CONST]SCOP2[0][3][1][2]: 0.15612494995996 Backup_Path[21] - R[0,3,1,2]
   = 0
 [CONST]SCOP2[0][3][1][3]: 0.15612494995996 Backup_Path[26]
   + 0.15612494995996 Backup_Path[27] - R[0,3,1,3] = 0
 [CONST]SCOP2[0][3][2][0]: - R[0,3,2,0] = 0
 [CONST]SCOP2[0][3][2][1]: 0.15612494995996 Backup_Path[36] - R[0,3,2,1]
   = 0
 [CONST]SCOP2[0][3][2][3]: 0.15612494995996 Backup_Path[41]
   + 0.15612494995996 Backup_Path[42] - R[0,3,2,3] = 0
 [CONST]SCOP2[0][3][3][0]: - R[0,3,3,0] = 0
 [CONST]SCOP2[0][3][3][1]: - R[0,3,3,1] = 0
 [CONST]SCOP2[0][3][3][2]: - R[0,3,3,2] = 0
 [CONST]SCOP2[1][0][0][1]: - R[1,0,0,1] = 0
 [CONST]SCOP2[1][0][0][2]: - R[1,0,0,2] = 0
 [CONST]SCOP2[1][0][0][3]: - R[1,0,0,3] = 0
 [CONST]SCOP2[1][0][1][0]: 0.15612494995996 Backup_Path[15] - R[1,0,1,0]
   = 0
 [CONST]SCOP2[1][0][1][2]: 0.15612494995996 Backup_Path[20]
   + 0.15612494995996 Backup_Path[21] - R[1,0,1,2] = 0
 [CONST]SCOP2[1][0][1][3]: 0.15612494995996 Backup_Path[25]
   + 0.15612494995996 Backup_Path[26] - R[1,0,1,3] = 0
 [CONST]SCOP2[1][0][2][0]: 0.15612494995996 Backup_Path[31]
   + 0.15612494995996 Backup_Path[34] - R[1,0,2,0] = 0
 [CONST]SCOP2[1][0][2][1]: - R[1,0,2,1] = 0
 [CONST]SCOP2[1][0][2][3]: 0.15612494995996 Backup_Path[42] - R[1,0,2,3]
   = 0
 [CONST]SCOP2[1][0][3][0]: 0.15612494995996 Backup_Path[46]
   + 0.15612494995996 Backup_Path[49] - R[1,0,3,0] = 0
 [CONST]SCOP2[1][0][3][1]: - R[1,0,3,1] = 0
 [CONST]SCOP2[1][0][3][2]: 0.15612494995996 Backup_Path[57] - R[1,0,3,2]
   = 0
 [CONST]SCOP2[1][2][0][1]: - R[1,2,0,1] = 0
 [CONST]SCOP2[1][2][0][2]: 0.15612494995996 Backup_Path[5]
   + 0.15612494995996 Backup_Path[8] - R[1,2,0,2] = 0
 [CONST]SCOP2[1][2][0][3]: 0.15612494995996 Backup_Path[10] - R[1,2,0,3]
   = 0
 [CONST]SCOP2[1][2][1][0]: 0.15612494995996 Backup_Path[16]
   + 0.15612494995996 Backup_Path[17] - R[1,2,1,0] = 0
 [CONST]SCOP2[1][2][1][2]: 0.15612494995996 Backup_Path[22] - R[1,2,1,2]
   = 0
 [CONST]SCOP2[1][2][1][3]: 0.15612494995996 Backup_Path[27]
   + 0.15612494995996 Backup_Path[28] - R[1,2,1,3] = 0
 [CONST]SCOP2[1][2][2][0]: - R[1,2,2,0] = 0
 [CONST]SCOP2[1][2][2][1]: - R[1,2,2,1] = 0
 [CONST]SCOP2[1][2][2][3]: - R[1,2,2,3] = 0
 [CONST]SCOP2[1][2][3][0]: 0.15612494995996 Backup_Path[47] - R[1,2,3,0]
   = 0
 [CONST]SCOP2[1][2][3][1]: - R[1,2,3,1] = 0
 [CONST]SCOP2[1][2][3][2]: 0.15612494995996 Backup_Path[55]
   + 0.15612494995996 Backup_Path[58] - R[1,2,3,2] = 0
 [CONST]SCOP2[1][3][0][1]: - R[1,3,0,1] = 0
 [CONST]SCOP2[1][3][0][2]: 0.15612494995996 Backup_Path[6] - R[1,3,0,2]
   = 0
 [CONST]SCOP2[1][3][0][3]: 0.15612494995996 Backup_Path[11]
   + 0.15612494995996 Backup_Path[12] - R[1,3,0,3] = 0
 [CONST]SCOP2[1][3][1][0]: 0.15612494995996 Backup_Path[18]
   + 0.15612494995996 Backup_Path[19] - R[1,3,1,0] = 0
 [CONST]SCOP2[1][3][1][2]: 0.15612494995996 Backup_Path[23]
   + 0.15612494995996 Backup_Path[24] - R[1,3,1,2] = 0
 [CONST]SCOP2[1][3][1][3]: 0.15612494995996 Backup_Path[29] - R[1,3,1,3]
   = 0
 [CONST]SCOP2[1][3][2][0]: 0.15612494995996 Backup_Path[32] - R[1,3,2,0]
   = 0
 [CONST]SCOP2[1][3][2][1]: - R[1,3,2,1] = 0
 [CONST]SCOP2[1][3][2][3]: 0.15612494995996 Backup_Path[40]
   + 0.15612494995996 Backup_Path[43] - R[1,3,2,3] = 0
 [CONST]SCOP2[1][3][3][0]: - R[1,3,3,0] = 0
 [CONST]SCOP2[1][3][3][1]: - R[1,3,3,1] = 0
 [CONST]SCOP2[1][3][3][2]: - R[1,3,3,2] = 0
 [CONST]SCOP2[2][0][0][1]: - R[2,0,0,1] = 0
 [CONST]SCOP2[2][0][0][2]: - R[2,0,0,2] = 0
 [CONST]SCOP2[2][0][0][3]: - R[2,0,0,3] = 0
 [CONST]SCOP2[2][0][1][0]: 0.15612494995996 Backup_Path[16]
   + 0.15612494995996 Backup_Path[19] - R[2,0,1,0] = 0
 [CONST]SCOP2[2][0][1][2]: - R[2,0,1,2] = 0
 [CONST]SCOP2[2][0][1][3]: 0.15612494995996 Backup_Path[27] - R[2,0,1,3]
   = 0
 [CONST]SCOP2[2][0][2][0]: 0.15612494995996 Backup_Path[30] - R[2,0,2,0]
   = 0
 [CONST]SCOP2[2][0][2][1]: 0.15612494995996 Backup_Path[35]
   + 0.15612494995996 Backup_Path[36] - R[2,0,2,1] = 0
 [CONST]SCOP2[2][0][2][3]: 0.15612494995996 Backup_Path[40]
   + 0.15612494995996 Backup_Path[41] - R[2,0,2,3] = 0
 [CONST]SCOP2[2][0][3][0]: 0.15612494995996 Backup_Path[47]
   + 0.15612494995996 Backup_Path[48] - R[2,0,3,0] = 0
 [CONST]SCOP2[2][0][3][1]: 0.15612494995996 Backup_Path[53] - R[2,0,3,1]
   = 0
 [CONST]SCOP2[2][0][3][2]: - R[2,0,3,2] = 0
 [CONST]SCOP2[2][1][0][1]: 0.15612494995996 Backup_Path[1]
   + 0.15612494995996 Backup_Path[4] - R[2,1,0,1] = 0
 [CONST]SCOP2[2][1][0][2]: - R[2,1,0,2] = 0
 [CONST]SCOP2[2][1][0][3]: 0.15612494995996 Backup_Path[12] - R[2,1,0,3]
   = 0
 [CONST]SCOP2[2][1][1][0]: - R[2,1,1,0] = 0
 [CONST]SCOP2[2][1][1][2]: - R[2,1,1,2] = 0
 [CONST]SCOP2[2][1][1][3]: - R[2,1,1,3] = 0
 [CONST]SCOP2[2][1][2][0]: 0.15612494995996 Backup_Path[31]
   + 0.15612494995996 Backup_Path[32] - R[2,1,2,0] = 0
 [CONST]SCOP2[2][1][2][1]: 0.15612494995996 Backup_Path[37] - R[2,1,2,1]
   = 0
 [CONST]SCOP2[2][1][2][3]: 0.15612494995996 Backup_Path[42]
   + 0.15612494995996 Backup_Path[43] - R[2,1,2,3] = 0
 [CONST]SCOP2[2][1][3][0]: 0.15612494995996 Backup_Path[49] - R[2,1,3,0]
   = 0
 [CONST]SCOP2[2][1][3][1]: 0.15612494995996 Backup_Path[51]
   + 0.15612494995996 Backup_Path[54] - R[2,1,3,1] = 0
 [CONST]SCOP2[2][1][3][2]: - R[2,1,3,2] = 0
 [CONST]SCOP2[2][3][0][1]: 0.15612494995996 Backup_Path[2] - R[2,3,0,1]
   = 0
 [CONST]SCOP2[2][3][0][2]: - R[2,3,0,2] = 0
 [CONST]SCOP2[2][3][0][3]: 0.15612494995996 Backup_Path[10]
   + 0.15612494995996 Backup_Path[13] - R[2,3,0,3] = 0
 [CONST]SCOP2[2][3][1][0]: 0.15612494995996 Backup_Path[17] - R[2,3,1,0]
   = 0
 [CONST]SCOP2[2][3][1][2]: - R[2,3,1,2] = 0
 [CONST]SCOP2[2][3][1][3]: 0.15612494995996 Backup_Path[25]
   + 0.15612494995996 Backup_Path[28] - R[2,3,1,3] = 0
 [CONST]SCOP2[2][3][2][0]: 0.15612494995996 Backup_Path[33]
   + 0.15612494995996 Backup_Path[34] - R[2,3,2,0] = 0
 [CONST]SCOP2[2][3][2][1]: 0.15612494995996 Backup_Path[38]
   + 0.15612494995996 Backup_Path[39] - R[2,3,2,1] = 0
 [CONST]SCOP2[2][3][2][3]: 0.15612494995996 Backup_Path[44] - R[2,3,2,3]
   = 0
 [CONST]SCOP2[2][3][3][0]: - R[2,3,3,0] = 0
 [CONST]SCOP2[2][3][3][1]: - R[2,3,3,1] = 0
 [CONST]SCOP2[2][3][3][2]: - R[2,3,3,2] = 0
 [CONST]SCOP2[3][0][0][1]: - R[3,0,0,1] = 0
 [CONST]SCOP2[3][0][0][2]: - R[3,0,0,2] = 0
 [CONST]SCOP2[3][0][0][3]: - R[3,0,0,3] = 0
 [CONST]SCOP2[3][0][1][0]: 0.15612494995996 Backup_Path[17]
   + 0.15612494995996 Backup_Path[18] - R[3,0,1,0] = 0
 [CONST]SCOP2[3][0][1][2]: 0.15612494995996 Backup_Path[23] - R[3,0,1,2]
   = 0
 [CONST]SCOP2[3][0][1][3]: - R[3,0,1,3] = 0
 [CONST]SCOP2[3][0][2][0]: 0.15612494995996 Backup_Path[32]
   + 0.15612494995996 Backup_Path[33] - R[3,0,2,0] = 0
 [CONST]SCOP2[3][0][2][1]: 0.15612494995996 Backup_Path[38] - R[3,0,2,1]
   = 0
 [CONST]SCOP2[3][0][2][3]: - R[3,0,2,3] = 0
 [CONST]SCOP2[3][0][3][0]: 0.15612494995996 Backup_Path[45] - R[3,0,3,0]
   = 0
 [CONST]SCOP2[3][0][3][1]: 0.15612494995996 Backup_Path[50]
   + 0.15612494995996 Backup_Path[51] - R[3,0,3,1] = 0
 [CONST]SCOP2[3][0][3][2]: 0.15612494995996 Backup_Path[55]
   + 0.15612494995996 Backup_Path[56] - R[3,0,3,2] = 0
 [CONST]SCOP2[3][1][0][1]: 0.15612494995996 Backup_Path[2]
   + 0.15612494995996 Backup_Path[3] - R[3,1,0,1] = 0
 [CONST]SCOP2[3][1][0][2]: 0.15612494995996 Backup_Path[8] - R[3,1,0,2]
   = 0
 [CONST]SCOP2[3][1][0][3]: - R[3,1,0,3] = 0
 [CONST]SCOP2[3][1][1][0]: - R[3,1,1,0] = 0
 [CONST]SCOP2[3][1][1][2]: - R[3,1,1,2] = 0
 [CONST]SCOP2[3][1][1][3]: - R[3,1,1,3] = 0
 [CONST]SCOP2[3][1][2][0]: 0.15612494995996 Backup_Path[34] - R[3,1,2,0]
   = 0
 [CONST]SCOP2[3][1][2][1]: 0.15612494995996 Backup_Path[36]
   + 0.15612494995996 Backup_Path[39] - R[3,1,2,1] = 0
 [CONST]SCOP2[3][1][2][3]: - R[3,1,2,3] = 0
 [CONST]SCOP2[3][1][3][0]: 0.15612494995996 Backup_Path[46]
   + 0.15612494995996 Backup_Path[47] - R[3,1,3,0] = 0
 [CONST]SCOP2[3][1][3][1]: 0.15612494995996 Backup_Path[52] - R[3,1,3,1]
   = 0
 [CONST]SCOP2[3][1][3][2]: 0.15612494995996 Backup_Path[57]
   + 0.15612494995996 Backup_Path[58] - R[3,1,3,2] = 0
 [CONST]SCOP2[3][2][0][1]: 0.15612494995996 Backup_Path[4] - R[3,2,0,1]
   = 0
 [CONST]SCOP2[3][2][0][2]: 0.15612494995996 Backup_Path[6]
   + 0.15612494995996 Backup_Path[9] - R[3,2,0,2] = 0
 [CONST]SCOP2[3][2][0][3]: - R[3,2,0,3] = 0
 [CONST]SCOP2[3][2][1][0]: 0.15612494995996 Backup_Path[19] - R[3,2,1,0]
   = 0
 [CONST]SCOP2[3][2][1][2]: 0.15612494995996 Backup_Path[21]
   + 0.15612494995996 Backup_Path[24] - R[3,2,1,2] = 0
 [CONST]SCOP2[3][2][1][3]: - R[3,2,1,3] = 0
 [CONST]SCOP2[3][2][2][0]: - R[3,2,2,0] = 0
 [CONST]SCOP2[3][2][2][1]: - R[3,2,2,1] = 0
 [CONST]SCOP2[3][2][2][3]: - R[3,2,2,3] = 0
 [CONST]SCOP2[3][2][3][0]: 0.15612494995996 Backup_Path[48]
   + 0.15612494995996 Backup_Path[49] - R[3,2,3,0] = 0
 [CONST]SCOP2[3][2][3][1]: 0.15612494995996 Backup_Path[53]
   + 0.15612494995996 Backup_Path[54] - R[3,2,3,1] = 0
 [CONST]SCOP2[3][2][3][2]: 0.15612494995996 Backup_Path[59] - R[3,2,3,2]
   = 0
 UniquePath[0,1]: Backup_Path[0] + Backup_Path[1] + Backup_Path[2]
   + Backup_Path[3] + Backup_Path[4] = 1
 UniquePath[0,2]: Backup_Path[5] + Backup_Path[6] + Backup_Path[7]
   + Backup_Path[8] + Backup_Path[9] = 1
 UniquePath[0,3]: Backup_Path[10] + Backup_Path[11] + Backup_Path[12]
   + Backup_Path[13] + Backup_Path[14] = 1
 UniquePath[1,0]: Backup_Path[15] + Backup_Path[16] + Backup_Path[17]
   + Backup_Path[18] + Backup_Path[19] = 1
 UniquePath[1,2]: Backup_Path[20] + Backup_Path[21] + Backup_Path[22]
   + Backup_Path[23] + Backup_Path[24] = 1
 UniquePath[1,3]: Backup_Path[25] + Backup_Path[26] + Backup_Path[27]
   + Backup_Path[28] + Backup_Path[29] = 1
 UniquePath[2,0]: Backup_Path[30] + Backup_Path[31] + Backup_Path[32]
   + Backup_Path[33] + Backup_Path[34] = 1
 UniquePath[2,1]: Backup_Path[35] + Backup_Path[36] + Backup_Path[37]
   + Backup_Path[38] + Backup_Path[39] = 1
 UniquePath[2,3]: Backup_Path[40] + Backup_Path[41] + Backup_Path[42]
   + Backup_Path[43] + Backup_Path[44] = 1
 UniquePath[3,0]: Backup_Path[45] + Backup_Path[46] + Backup_Path[47]
   + Backup_Path[48] + Backup_Path[49] = 1
 UniquePath[3,1]: Backup_Path[50] + Backup_Path[51] + Backup_Path[52]
   + Backup_Path[53] + Backup_Path[54] = 1
 UniquePath[3,2]: Backup_Path[55] + Backup_Path[56] + Backup_Path[57]
   + Backup_Path[58] + Backup_Path[59] = 1
 [CONST]SCOP1[0][1]: [ - U[0,1] ^2 + R[0,1,0,1] ^2 + R[0,1,0,2] ^2
   + R[0,1,0,3] ^2 + R[0,1,1,0] ^2 + R[0,1,1,2] ^2 + R[0,1,1,3] ^2
   + R[0,1,2,0] ^2 + R[0,1,2,1] ^2 + R[0,1,2,3] ^2 + R[0,1,3,0] ^2
   + R[0,1,3,1] ^2 + R[0,1,3,2] ^2 ] <= 0
 [CONST]SCOP1[0][2]: [ - U[0,2] ^2 + R[0,2,0,1] ^2 + R[0,2,0,2] ^2
   + R[0,2,0,3] ^2 + R[0,2,1,0] ^2 + R[0,2,1,2] ^2 + R[0,2,1,3] ^2
   + R[0,2,2,0] ^2 + R[0,2,2,1] ^2 + R[0,2,2,3] ^2 + R[0,2,3,0] ^2
   + R[0,2,3,1] ^2 + R[0,2,3,2] ^2 ] <= 0
 [CONST]SCOP1[0][3]: [ - U[0,3] ^2 + R[0,3,0,1] ^2 + R[0,3,0,2] ^2
   + R[0,3,0,3] ^2 + R[0,3,1,0] ^2 + R[0,3,1,2] ^2 + R[0,3,1,3] ^2
   + R[0,3,2,0] ^2 + R[0,3,2,1] ^2 + R[0,3,2,3] ^2 + R[0,3,3,0] ^2
   + R[0,3,3,1] ^2 + R[0,3,3,2] ^2 ] <= 0
 [CONST]SCOP1[1][0]: [ - U[1,0] ^2 + R[1,0,0,1] ^2 + R[1,0,0,2] ^2
   + R[1,0,0,3] ^2 + R[1,0,1,0] ^2 + R[1,0,1,2] ^2 + R[1,0,1,3] ^2
   + R[1,0,2,0] ^2 + R[1,0,2,1] ^2 + R[1,0,2,3] ^2 + R[1,0,3,0] ^2
   + R[1,0,3,1] ^2 + R[1,0,3,2] ^2 ] <= 0
 [CONST]SCOP1[1][2]: [ - U[1,2] ^2 + R[1,2,0,1] ^2 + R[1,2,0,2] ^2
   + R[1,2,0,3] ^2 + R[1,2,1,0] ^2 + R[1,2,1,2] ^2 + R[1,2,1,3] ^2
   + R[1,2,2,0] ^2 + R[1,2,2,1] ^2 + R[1,2,2,3] ^2 + R[1,2,3,0] ^2
   + R[1,2,3,1] ^2 + R[1,2,3,2] ^2 ] <= 0
 [CONST]SCOP1[1][3]: [ - U[1,3] ^2 + R[1,3,0,1] ^2 + R[1,3,0,2] ^2
   + R[1,3,0,3] ^2 + R[1,3,1,0] ^2 + R[1,3,1,2] ^2 + R[1,3,1,3] ^2
   + R[1,3,2,0] ^2 + R[1,3,2,1] ^2 + R[1,3,2,3] ^2 + R[1,3,3,0] ^2
   + R[1,3,3,1] ^2 + R[1,3,3,2] ^2 ] <= 0
 [CONST]SCOP1[2][0]: [ - U[2,0] ^2 + R[2,0,0,1] ^2 + R[2,0,0,2] ^2
   + R[2,0,0,3] ^2 + R[2,0,1,0] ^2 + R[2,0,1,2] ^2 + R[2,0,1,3] ^2
   + R[2,0,2,0] ^2 + R[2,0,2,1] ^2 + R[2,0,2,3] ^2 + R[2,0,3,0] ^2
   + R[2,0,3,1] ^2 + R[2,0,3,2] ^2 ] <= 0
 [CONST]SCOP1[2][1]: [ - U[2,1] ^2 + R[2,1,0,1] ^2 + R[2,1,0,2] ^2
   + R[2,1,0,3] ^2 + R[2,1,1,0] ^2 + R[2,1,1,2] ^2 + R[2,1,1,3] ^2
   + R[2,1,2,0] ^2 + R[2,1,2,1] ^2 + R[2,1,2,3] ^2 + R[2,1,3,0] ^2
   + R[2,1,3,1] ^2 + R[2,1,3,2] ^2 ] <= 0
 [CONST]SCOP1[2][3]: [ - U[2,3] ^2 + R[2,3,0,1] ^2 + R[2,3,0,2] ^2
   + R[2,3,0,3] ^2 + R[2,3,1,0] ^2 + R[2,3,1,2] ^2 + R[2,3,1,3] ^2
   + R[2,3,2,0] ^2 + R[2,3,2,1] ^2 + R[2,3,2,3] ^2 + R[2,3,3,0] ^2
   + R[2,3,3,1] ^2 + R[2,3,3,2] ^2 ] <= 0
 [CONST]SCOP1[3][0]: [ - U[3,0] ^2 + R[3,0,0,1] ^2 + R[3,0,0,2] ^2
   + R[3,0,0,3] ^2 + R[3,0,1,0] ^2 + R[3,0,1,2] ^2 + R[3,0,1,3] ^2
   + R[3,0,2,0] ^2 + R[3,0,2,1] ^2 + R[3,0,2,3] ^2 + R[3,0,3,0] ^2
   + R[3,0,3,1] ^2 + R[3,0,3,2] ^2 ] <= 0
 [CONST]SCOP1[3][1]: [ - U[3,1] ^2 + R[3,1,0,1] ^2 + R[3,1,0,2] ^2
   + R[3,1,0,3] ^2 + R[3,1,1,0] ^2 + R[3,1,1,2] ^2 + R[3,1,1,3] ^2
   + R[3,1,2,0] ^2 + R[3,1,2,1] ^2 + R[3,1,2,3] ^2 + R[3,1,3,0] ^2
   + R[3,1,3,1] ^2 + R[3,1,3,2] ^2 ] <= 0
 [CONST]SCOP1[3][2]: [ - U[3,2] ^2 + R[3,2,0,1] ^2 + R[3,2,0,2] ^2
   + R[3,2,0,3] ^2 + R[3,2,1,0] ^2 + R[3,2,1,2] ^2 + R[3,2,1,3] ^2
   + R[3,2,2,0] ^2 + R[3,2,2,1] ^2 + R[3,2,2,3] ^2 + R[3,2,3,0] ^2
   + R[3,2,3,1] ^2 + R[3,2,3,2] ^2 ] <= 0
Bounds
Binaries
 Backup_Path[0] Backup_Path[1] Backup_Path[2] Backup_Path[3] Backup_Path[4]
 Backup_Path[5] Backup_Path[6] Backup_Path[7] Backup_Path[8] Backup_Path[9]
 Backup_Path[10] Backup_Path[11] Backup_Path[12] Backup_Path[13]
 Backup_Path[14] Backup_Path[15] Backup_Path[16] Backup_Path[17]
 Backup_Path[18] Backup_Path[19] Backup_Path[20] Backup_Path[21]
 Backup_Path[22] Backup_Path[23] Backup_Path[24] Backup_Path[25]
 Backup_Path[26] Backup_Path[27] Backup_Path[28] Backup_Path[29]
 Backup_Path[30] Backup_Path[31] Backup_Path[32] Backup_Path[33]
 Backup_Path[34] Backup_Path[35] Backup_Path[36] Backup_Path[37]
 Backup_Path[38] Backup_Path[39] Backup_Path[40] Backup_Path[41]
 Backup_Path[42] Backup_Path[43] Backup_Path[44] Backup_Path[45]
 Backup_Path[46] Backup_Path[47] Backup_Path[48] Backup_Path[49]
 Backup_Path[50] Backup_Path[51] Backup_Path[52] Backup_Path[53]
 Backup_Path[54] Backup_Path[55] Backup_Path[56] Backup_Path[57]
 Backup_Path[58] Backup_Path[59]
End
