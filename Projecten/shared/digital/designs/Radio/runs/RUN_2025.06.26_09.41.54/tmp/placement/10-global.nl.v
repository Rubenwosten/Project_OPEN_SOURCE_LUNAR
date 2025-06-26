module radio (Rx,
    Tx,
    busy,
    clk,
    enable,
    receive,
    send,
    rx_data,
    tx_data);
 input Rx;
 output Tx;
 output busy;
 input clk;
 input enable;
 input receive;
 input send;
 output [7:0] rx_data;
 input [7:0] tx_data;

 wire _000_;
 wire _001_;
 wire _002_;
 wire _003_;
 wire _004_;
 wire _005_;
 wire _006_;
 wire _007_;
 wire _008_;
 wire _009_;
 wire _010_;
 wire _011_;
 wire _012_;
 wire _013_;
 wire _014_;
 wire _015_;
 wire _016_;
 wire _017_;
 wire _018_;
 wire _019_;
 wire _020_;
 wire _021_;
 wire _022_;
 wire _023_;
 wire _024_;
 wire _025_;
 wire _026_;
 wire _027_;
 wire _028_;
 wire _029_;
 wire _030_;
 wire _031_;
 wire _032_;
 wire _033_;
 wire _034_;
 wire _035_;
 wire _036_;
 wire _037_;
 wire _038_;
 wire _039_;
 wire _040_;
 wire _041_;
 wire _042_;
 wire _043_;
 wire _044_;
 wire _045_;
 wire _046_;
 wire _047_;
 wire _048_;
 wire _049_;
 wire _050_;
 wire _051_;
 wire _052_;
 wire _053_;
 wire _054_;
 wire _055_;
 wire _056_;
 wire _057_;
 wire _058_;
 wire _059_;
 wire _060_;
 wire _061_;
 wire _062_;
 wire _063_;
 wire _064_;
 wire _065_;
 wire _066_;
 wire _067_;
 wire _068_;
 wire _069_;
 wire _070_;
 wire _071_;
 wire _072_;
 wire _073_;
 wire _074_;
 wire _075_;
 wire _076_;
 wire _077_;
 wire \rx_bit_cnt[0] ;
 wire \rx_bit_cnt[1] ;
 wire \rx_bit_cnt[2] ;
 wire rx_busy;
 wire \rx_shift_reg[0] ;
 wire \rx_shift_reg[1] ;
 wire \rx_shift_reg[2] ;
 wire \rx_shift_reg[3] ;
 wire \rx_shift_reg[4] ;
 wire \rx_shift_reg[5] ;
 wire \rx_shift_reg[6] ;
 wire \rx_shift_reg[7] ;
 wire \tx_bit_cnt[0] ;
 wire \tx_bit_cnt[1] ;
 wire \tx_bit_cnt[2] ;
 wire tx_busy;
 wire \tx_shift_reg[0] ;
 wire \tx_shift_reg[1] ;
 wire \tx_shift_reg[2] ;
 wire \tx_shift_reg[3] ;
 wire \tx_shift_reg[4] ;
 wire \tx_shift_reg[5] ;
 wire \tx_shift_reg[6] ;
 wire \tx_shift_reg[7] ;

 sky130_fd_sc_hd__buf_1 _078_ (.A(rx_busy),
    .X(_062_));
 sky130_fd_sc_hd__buf_1 _079_ (.A(tx_busy),
    .X(_063_));
 sky130_fd_sc_hd__or2_2 _080_ (.A(_062_),
    .B(_063_),
    .X(busy));
 sky130_fd_sc_hd__buf_1 _081_ (.A(enable),
    .X(_064_));
 sky130_fd_sc_hd__nor2b_2 _082_ (.A(tx_busy),
    .B_N(send),
    .Y(_065_));
 sky130_fd_sc_hd__nor2_2 _083_ (.A(_063_),
    .B(send),
    .Y(_066_));
 sky130_fd_sc_hd__and2_2 _084_ (.A(\tx_shift_reg[1] ),
    .B(_063_),
    .X(_067_));
 sky130_fd_sc_hd__a221o_2 _085_ (.A1(tx_data[0]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[0] ),
    .C1(_067_),
    .X(_068_));
 sky130_fd_sc_hd__and2_2 _086_ (.A(_064_),
    .B(_068_),
    .X(_000_));
 sky130_fd_sc_hd__and2_2 _087_ (.A(\tx_shift_reg[2] ),
    .B(tx_busy),
    .X(_069_));
 sky130_fd_sc_hd__a221o_2 _088_ (.A1(tx_data[1]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[1] ),
    .C1(_069_),
    .X(_070_));
 sky130_fd_sc_hd__and2_2 _089_ (.A(_064_),
    .B(_070_),
    .X(_001_));
 sky130_fd_sc_hd__and2_2 _090_ (.A(\tx_shift_reg[3] ),
    .B(tx_busy),
    .X(_071_));
 sky130_fd_sc_hd__a221o_2 _091_ (.A1(tx_data[2]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[2] ),
    .C1(_071_),
    .X(_072_));
 sky130_fd_sc_hd__and2_2 _092_ (.A(_064_),
    .B(_072_),
    .X(_002_));
 sky130_fd_sc_hd__buf_1 _093_ (.A(enable),
    .X(_073_));
 sky130_fd_sc_hd__and2_2 _094_ (.A(\tx_shift_reg[4] ),
    .B(tx_busy),
    .X(_074_));
 sky130_fd_sc_hd__a221o_2 _095_ (.A1(tx_data[3]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[3] ),
    .C1(_074_),
    .X(_075_));
 sky130_fd_sc_hd__and2_2 _096_ (.A(_073_),
    .B(_075_),
    .X(_003_));
 sky130_fd_sc_hd__and2_2 _097_ (.A(\tx_shift_reg[5] ),
    .B(tx_busy),
    .X(_076_));
 sky130_fd_sc_hd__a221o_2 _098_ (.A1(tx_data[4]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[4] ),
    .C1(_076_),
    .X(_077_));
 sky130_fd_sc_hd__and2_2 _099_ (.A(_073_),
    .B(_077_),
    .X(_004_));
 sky130_fd_sc_hd__and2_2 _100_ (.A(\tx_shift_reg[6] ),
    .B(tx_busy),
    .X(_033_));
 sky130_fd_sc_hd__a221o_2 _101_ (.A1(tx_data[5]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[5] ),
    .C1(_033_),
    .X(_034_));
 sky130_fd_sc_hd__and2_2 _102_ (.A(_073_),
    .B(_034_),
    .X(_005_));
 sky130_fd_sc_hd__and2_2 _103_ (.A(\tx_shift_reg[7] ),
    .B(tx_busy),
    .X(_035_));
 sky130_fd_sc_hd__a221o_2 _104_ (.A1(tx_data[6]),
    .A2(_065_),
    .B1(_066_),
    .B2(\tx_shift_reg[6] ),
    .C1(_035_),
    .X(_036_));
 sky130_fd_sc_hd__and2_2 _105_ (.A(_073_),
    .B(_036_),
    .X(_006_));
 sky130_fd_sc_hd__nor2_2 _106_ (.A(rx_busy),
    .B(receive),
    .Y(_037_));
 sky130_fd_sc_hd__and3_2 _107_ (.A(\rx_bit_cnt[2] ),
    .B(\rx_bit_cnt[1] ),
    .C(\rx_bit_cnt[0] ),
    .X(_038_));
 sky130_fd_sc_hd__a21boi_2 _108_ (.A1(rx_busy),
    .A2(_038_),
    .B1_N(enable),
    .Y(_039_));
 sky130_fd_sc_hd__and2b_2 _109_ (.A_N(_037_),
    .B(_039_),
    .X(_007_));
 sky130_fd_sc_hd__and3_2 _110_ (.A(rx_busy),
    .B(enable),
    .C(_038_),
    .X(_040_));
 sky130_fd_sc_hd__a22o_2 _111_ (.A1(rx_data[0]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[0] ),
    .X(_008_));
 sky130_fd_sc_hd__a22o_2 _112_ (.A1(rx_data[1]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[1] ),
    .X(_009_));
 sky130_fd_sc_hd__a22o_2 _113_ (.A1(rx_data[2]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[2] ),
    .X(_010_));
 sky130_fd_sc_hd__a22o_2 _114_ (.A1(rx_data[3]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[3] ),
    .X(_011_));
 sky130_fd_sc_hd__a22o_2 _115_ (.A1(rx_data[4]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[4] ),
    .X(_012_));
 sky130_fd_sc_hd__a22o_2 _116_ (.A1(rx_data[5]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[5] ),
    .X(_013_));
 sky130_fd_sc_hd__a22o_2 _117_ (.A1(rx_data[6]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[6] ),
    .X(_014_));
 sky130_fd_sc_hd__a22o_2 _118_ (.A1(rx_data[7]),
    .A2(_039_),
    .B1(_040_),
    .B2(\rx_shift_reg[7] ),
    .X(_015_));
 sky130_fd_sc_hd__o21ai_2 _119_ (.A1(_063_),
    .A2(send),
    .B1(\tx_bit_cnt[0] ),
    .Y(_041_));
 sky130_fd_sc_hd__o211a_2 _120_ (.A1(\tx_bit_cnt[0] ),
    .A2(_063_),
    .B1(_064_),
    .C1(_041_),
    .X(_016_));
 sky130_fd_sc_hd__nand2_2 _121_ (.A(\tx_bit_cnt[1] ),
    .B(\tx_bit_cnt[0] ),
    .Y(_042_));
 sky130_fd_sc_hd__a22o_2 _122_ (.A1(\tx_bit_cnt[1] ),
    .A2(_066_),
    .B1(_042_),
    .B2(_063_),
    .X(_043_));
 sky130_fd_sc_hd__o211a_2 _123_ (.A1(\tx_bit_cnt[1] ),
    .A2(\tx_bit_cnt[0] ),
    .B1(_064_),
    .C1(_043_),
    .X(_017_));
 sky130_fd_sc_hd__o211a_2 _124_ (.A1(_063_),
    .A2(send),
    .B1(\tx_bit_cnt[1] ),
    .C1(\tx_bit_cnt[0] ),
    .X(_044_));
 sky130_fd_sc_hd__inv_2 _125_ (.A(\tx_bit_cnt[2] ),
    .Y(_045_));
 sky130_fd_sc_hd__o21a_2 _126_ (.A1(_045_),
    .A2(_042_),
    .B1(_063_),
    .X(_046_));
 sky130_fd_sc_hd__o221a_2 _127_ (.A1(\tx_bit_cnt[2] ),
    .A2(_044_),
    .B1(_046_),
    .B2(_066_),
    .C1(_064_),
    .X(_018_));
 sky130_fd_sc_hd__or2b_2 _128_ (.A(tx_data[7]),
    .B_N(send),
    .X(_047_));
 sky130_fd_sc_hd__inv_2 _129_ (.A(_063_),
    .Y(_048_));
 sky130_fd_sc_hd__o2111a_2 _130_ (.A1(\tx_shift_reg[7] ),
    .A2(send),
    .B1(_047_),
    .C1(_048_),
    .D1(_064_),
    .X(_019_));
 sky130_fd_sc_hd__and3_2 _131_ (.A(\tx_shift_reg[0] ),
    .B(_063_),
    .C(enable),
    .X(_020_));
 sky130_fd_sc_hd__o21ai_2 _132_ (.A1(_062_),
    .A2(receive),
    .B1(\rx_bit_cnt[0] ),
    .Y(_049_));
 sky130_fd_sc_hd__o211a_2 _133_ (.A1(\rx_bit_cnt[0] ),
    .A2(_062_),
    .B1(_064_),
    .C1(_049_),
    .X(_021_));
 sky130_fd_sc_hd__nand2_2 _134_ (.A(\rx_bit_cnt[1] ),
    .B(\rx_bit_cnt[0] ),
    .Y(_050_));
 sky130_fd_sc_hd__a22o_2 _135_ (.A1(_062_),
    .A2(_050_),
    .B1(_037_),
    .B2(\rx_bit_cnt[1] ),
    .X(_051_));
 sky130_fd_sc_hd__o211a_2 _136_ (.A1(\rx_bit_cnt[1] ),
    .A2(\rx_bit_cnt[0] ),
    .B1(_064_),
    .C1(_051_),
    .X(_022_));
 sky130_fd_sc_hd__inv_2 _137_ (.A(receive),
    .Y(_052_));
 sky130_fd_sc_hd__a31o_2 _138_ (.A1(\rx_bit_cnt[1] ),
    .A2(\rx_bit_cnt[0] ),
    .A3(_062_),
    .B1(\rx_bit_cnt[2] ),
    .X(_053_));
 sky130_fd_sc_hd__o211a_2 _139_ (.A1(_062_),
    .A2(_052_),
    .B1(_039_),
    .C1(_053_),
    .X(_023_));
 sky130_fd_sc_hd__a22o_2 _140_ (.A1(\rx_shift_reg[1] ),
    .A2(_062_),
    .B1(_037_),
    .B2(\rx_shift_reg[0] ),
    .X(_054_));
 sky130_fd_sc_hd__and2_2 _141_ (.A(_073_),
    .B(_054_),
    .X(_024_));
 sky130_fd_sc_hd__a22o_2 _142_ (.A1(\rx_shift_reg[2] ),
    .A2(_062_),
    .B1(_037_),
    .B2(\rx_shift_reg[1] ),
    .X(_055_));
 sky130_fd_sc_hd__and2_2 _143_ (.A(_073_),
    .B(_055_),
    .X(_025_));
 sky130_fd_sc_hd__a22o_2 _144_ (.A1(\rx_shift_reg[3] ),
    .A2(_062_),
    .B1(_037_),
    .B2(\rx_shift_reg[2] ),
    .X(_056_));
 sky130_fd_sc_hd__and2_2 _145_ (.A(_073_),
    .B(_056_),
    .X(_026_));
 sky130_fd_sc_hd__a22o_2 _146_ (.A1(\rx_shift_reg[4] ),
    .A2(rx_busy),
    .B1(_037_),
    .B2(\rx_shift_reg[3] ),
    .X(_057_));
 sky130_fd_sc_hd__and2_2 _147_ (.A(_073_),
    .B(_057_),
    .X(_027_));
 sky130_fd_sc_hd__a22o_2 _148_ (.A1(\rx_shift_reg[5] ),
    .A2(rx_busy),
    .B1(_037_),
    .B2(\rx_shift_reg[4] ),
    .X(_058_));
 sky130_fd_sc_hd__and2_2 _149_ (.A(_073_),
    .B(_058_),
    .X(_028_));
 sky130_fd_sc_hd__a22o_2 _150_ (.A1(\rx_shift_reg[6] ),
    .A2(rx_busy),
    .B1(_037_),
    .B2(\rx_shift_reg[5] ),
    .X(_059_));
 sky130_fd_sc_hd__and2_2 _151_ (.A(_073_),
    .B(_059_),
    .X(_029_));
 sky130_fd_sc_hd__a22o_2 _152_ (.A1(\rx_shift_reg[7] ),
    .A2(rx_busy),
    .B1(_037_),
    .B2(\rx_shift_reg[6] ),
    .X(_060_));
 sky130_fd_sc_hd__and2_2 _153_ (.A(enable),
    .B(_060_),
    .X(_030_));
 sky130_fd_sc_hd__a22o_2 _154_ (.A1(_062_),
    .A2(Rx),
    .B1(_037_),
    .B2(\rx_shift_reg[7] ),
    .X(_061_));
 sky130_fd_sc_hd__and2_2 _155_ (.A(enable),
    .B(_061_),
    .X(_031_));
 sky130_fd_sc_hd__o21a_2 _156_ (.A1(_065_),
    .A2(_046_),
    .B1(_064_),
    .X(_032_));
 sky130_fd_sc_hd__dfxtp_2 _157_ (.CLK(clk),
    .D(_000_),
    .Q(\tx_shift_reg[0] ));
 sky130_fd_sc_hd__dfxtp_2 _158_ (.CLK(clk),
    .D(_001_),
    .Q(\tx_shift_reg[1] ));
 sky130_fd_sc_hd__dfxtp_2 _159_ (.CLK(clk),
    .D(_002_),
    .Q(\tx_shift_reg[2] ));
 sky130_fd_sc_hd__dfxtp_2 _160_ (.CLK(clk),
    .D(_003_),
    .Q(\tx_shift_reg[3] ));
 sky130_fd_sc_hd__dfxtp_2 _161_ (.CLK(clk),
    .D(_004_),
    .Q(\tx_shift_reg[4] ));
 sky130_fd_sc_hd__dfxtp_2 _162_ (.CLK(clk),
    .D(_005_),
    .Q(\tx_shift_reg[5] ));
 sky130_fd_sc_hd__dfxtp_2 _163_ (.CLK(clk),
    .D(_006_),
    .Q(\tx_shift_reg[6] ));
 sky130_fd_sc_hd__dfxtp_2 _164_ (.CLK(clk),
    .D(_007_),
    .Q(rx_busy));
 sky130_fd_sc_hd__dfxtp_2 _165_ (.CLK(clk),
    .D(_008_),
    .Q(rx_data[0]));
 sky130_fd_sc_hd__dfxtp_2 _166_ (.CLK(clk),
    .D(_009_),
    .Q(rx_data[1]));
 sky130_fd_sc_hd__dfxtp_2 _167_ (.CLK(clk),
    .D(_010_),
    .Q(rx_data[2]));
 sky130_fd_sc_hd__dfxtp_2 _168_ (.CLK(clk),
    .D(_011_),
    .Q(rx_data[3]));
 sky130_fd_sc_hd__dfxtp_2 _169_ (.CLK(clk),
    .D(_012_),
    .Q(rx_data[4]));
 sky130_fd_sc_hd__dfxtp_2 _170_ (.CLK(clk),
    .D(_013_),
    .Q(rx_data[5]));
 sky130_fd_sc_hd__dfxtp_2 _171_ (.CLK(clk),
    .D(_014_),
    .Q(rx_data[6]));
 sky130_fd_sc_hd__dfxtp_2 _172_ (.CLK(clk),
    .D(_015_),
    .Q(rx_data[7]));
 sky130_fd_sc_hd__dfxtp_2 _173_ (.CLK(clk),
    .D(_016_),
    .Q(\tx_bit_cnt[0] ));
 sky130_fd_sc_hd__dfxtp_2 _174_ (.CLK(clk),
    .D(_017_),
    .Q(\tx_bit_cnt[1] ));
 sky130_fd_sc_hd__dfxtp_2 _175_ (.CLK(clk),
    .D(_018_),
    .Q(\tx_bit_cnt[2] ));
 sky130_fd_sc_hd__dfxtp_2 _176_ (.CLK(clk),
    .D(_019_),
    .Q(\tx_shift_reg[7] ));
 sky130_fd_sc_hd__dfxtp_2 _177_ (.CLK(clk),
    .D(_020_),
    .Q(Tx));
 sky130_fd_sc_hd__dfxtp_2 _178_ (.CLK(clk),
    .D(_021_),
    .Q(\rx_bit_cnt[0] ));
 sky130_fd_sc_hd__dfxtp_2 _179_ (.CLK(clk),
    .D(_022_),
    .Q(\rx_bit_cnt[1] ));
 sky130_fd_sc_hd__dfxtp_2 _180_ (.CLK(clk),
    .D(_023_),
    .Q(\rx_bit_cnt[2] ));
 sky130_fd_sc_hd__dfxtp_2 _181_ (.CLK(clk),
    .D(_024_),
    .Q(\rx_shift_reg[0] ));
 sky130_fd_sc_hd__dfxtp_2 _182_ (.CLK(clk),
    .D(_025_),
    .Q(\rx_shift_reg[1] ));
 sky130_fd_sc_hd__dfxtp_2 _183_ (.CLK(clk),
    .D(_026_),
    .Q(\rx_shift_reg[2] ));
 sky130_fd_sc_hd__dfxtp_2 _184_ (.CLK(clk),
    .D(_027_),
    .Q(\rx_shift_reg[3] ));
 sky130_fd_sc_hd__dfxtp_2 _185_ (.CLK(clk),
    .D(_028_),
    .Q(\rx_shift_reg[4] ));
 sky130_fd_sc_hd__dfxtp_2 _186_ (.CLK(clk),
    .D(_029_),
    .Q(\rx_shift_reg[5] ));
 sky130_fd_sc_hd__dfxtp_2 _187_ (.CLK(clk),
    .D(_030_),
    .Q(\rx_shift_reg[6] ));
 sky130_fd_sc_hd__dfxtp_2 _188_ (.CLK(clk),
    .D(_031_),
    .Q(\rx_shift_reg[7] ));
 sky130_fd_sc_hd__dfxtp_2 _189_ (.CLK(clk),
    .D(_032_),
    .Q(tx_busy));
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Right_0 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Right_1 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Right_2 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Right_3 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Right_4 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Right_5 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Right_6 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Right_7 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Right_8 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Right_9 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Right_10 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_11_Right_11 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_12_Right_12 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_13_Right_13 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_14_Right_14 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_15_Right_15 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_16_Right_16 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_17_Right_17 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_18_Right_18 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Left_19 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Left_20 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Left_21 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Left_22 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Left_23 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Left_24 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Left_25 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Left_26 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Left_27 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Left_28 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Left_29 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_11_Left_30 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_12_Left_31 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_13_Left_32 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_14_Left_33 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_15_Left_34 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_16_Left_35 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_17_Left_36 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_18_Left_37 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_38 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_39 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_40 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_1_41 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_42 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_43 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_3_44 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_45 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_46 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_5_47 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_48 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_49 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_7_50 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_51 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_52 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_9_53 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_54 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_55 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_11_56 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_12_57 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_12_58 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_13_59 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_14_60 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_14_61 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_15_62 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_16_63 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_16_64 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_17_65 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_66 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_67 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_68 ();
endmodule
