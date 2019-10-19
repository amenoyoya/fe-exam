```
; 64ビット符号なし整数を加算するプログラム
ADD64 START
      RPUSH ; GR1〜7の内容をスタックに退避
      LD GR0,=0 ; 戻り値GR0を0初期化
      LAD GR3,3,GR1 ; GR3 = address(GR1[3])
      LAD GR4,3,GR2 ; GR4 = address(GR2[3])
      ; ループ開始: 16ビットごとの加算を下位から実行
LOOP  LD GR5,=0 ; 桁上がり用バッファ: GR5 = 0
      ADDL GR0,0,GR3 ; unsigned GR0 += value(GR3)
      JOV OV1 ; オーバフローが起こったらOV1にジャンプ
      JUMP NOV1 ; NOV1にジャンプ
OV1   LD,GR5,=1 ; オーバフローが起きたら GR5 = 1
NOV1  ADDL GR0,0,GR4 ; unsigned GR0 += value(GR4)
      JOV OV2 ; オーバフローが起こったらOV2にジャンプ
      JUMP NOV2 ; NOV2にジャンプ
OV2   LD,GR5,=1 ; オーバフローが起きたら GR5 = 1
NOV2  ST GR0,0,GR3 ; 加算結果をGR3ポインタに格納
      LD GR0,GR5 ; 桁上がりバッファをGR0にセット
      ; GR3ポインタがGR1(先頭アドレス)に達したらループ終了
      CPL GR3,GR1 ; unsigned GR3 - GR1 => FLAG
      JZE EXIT ; FLAG == 0 -jump-> EXIT
      SUBL GR3,=1 ; GR3ポインタをデクリメント
      SUBL GR4,=1 ; GR4ポインタをデクリメント
      JUMP LOOP ; ループ継続
      RPOP ; GR1〜7の内容をスタックから戻す
      RET ; 呼び出し元に戻る
      END
```

2進数の乗算は、乗数が0になるまで以下の手順を繰り返せば良い

1. 乗数の最下位ビットが1なら、被乗数の値を乗算結果に加算
2. 被乗数を1ビット左シフト（被乗数を倍にする）
3. 乗数を1ビットを右シフト（乗数を半分にする）

```
; 32ビット符号なし整数の乗算を行うプログラム
MUL32 START
      RPUSH ; GR1〜7の内容をスタックに退避
      LAD GR7,TEMP ; GR7にTEMPの先頭アドレスをセット
      ; 被乗数の値をTEMPから始まる4語の領域の下位2語に格納
      LD GR0,0,GR1 ; GR0 = value(GR1[0])
      ST GR0,2,GR7 ; GR0 => address(GR7[2])
      LD GR0,1,GR1 ; GR0 = value(GR1[1])
      ST GR0,3,GR7 ; GR0 => address(GR[7])
      LD GR0,=0 ; GR0 = 0
      ; TEMPから始まる4語の領域の上位2語にGR0(0)を格納
      ST GR0,0,GR7
      ST GR0,1,GR7
      ; GR3から始まる4語の領域にGR0(0)を格納
      ST GR0,0,GR3
      ST GR0,1,GR3
      ST GR0,2,GR3
      ST GR0,3,GR3
      LD GR5,=0 ; ループカウンタ: GR5 = 0
      ; 下位1ビット〜上位1ビットまで32ビット分ループ
LOOP  LD GR4,GR2 ; 乗数の先頭アドレス(GR2)をGR4に退避
      LD GR6,GR5 ; GR6 = GR5(ループカウンタ)
      ; 上位ビットの計算なら
      SUBL GR6,16 ; unsigned GR6 -= 16 => FLAG
      JMI LOWORD ; FLAG < 0 -jump-> LOWORD
      LD GR0,0,GR2 ; GR0 = value(GR2[0])
      SRL GR0,0,GR6 ; GR0(乗数)を ループカウンタ-16 の分だけ右シフト
      JUMP TEST ; TESTにジャンプ
      ; GR6 < 16: 下位ビットの計算なら
LOW   LD GR0,1,GR2  ; GR0 = value(GR2[1])
      SRL GR0,0,GR5 ; GR0(乗数)を ループカウンタ の分だけ右シフト
      ; GR0(乗数)の最下位1ビットが1なら
TEST  AND GR0,=#0001 ; GR0 AND 0001 => FLAG
      JZE EXIT ; FLAG == 0 -jump-> NEXT: 次のビットへ
      LD GR1,GR3 ; GR1(乗算結果) = GR3(被乗数)
      LAD GR2,TEMP ; GR2にTEMPの先頭アドレス(乗数)をセット
      CALL ADD64 ; 64ビット符号なし加算を実行 => GR1(乗算結果)
      ; ループカウンタが31ならループ終了
NEXT  CPL GR5,=31 ; unsigned GR5 - 31 => FLAG
      JZE EXIT ; FLAG == 0 -jump-> EXIT
      ADDL GR5,=1 ; ループカウンタをインクリメント
      ; 被乗数を左に1ビットシフト（TEMPを2倍にする）
      ; => GR1, GR2 にTEMPをセットしてADD64を呼ぶ
      LAD GR1,TEMP
      LAD GR2,TEMP
      CALL ADD64 ; GR1 = 2 * TEMP
      LD GR2,GR4 ; GR4に退避したアドレスをGR2に戻す
      JUMP LOOP ; ループ継続
EXIT  RPOP ; GR1〜7の内容をスタックから戻す
      RET ; 呼び出し元に戻る
      END

; 乗算結果の64ビット符号なし整数用の領域確保
TEMP DS 4
     END
```
