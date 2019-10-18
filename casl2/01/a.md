```
; メインプログラム
MAIN START
     RPUSH ; GR1〜7の内容をスタックに退避
     CALL DAYOFFST ; 副プログラム DAYOFFST 呼び出し
     RPOP ; GR1〜7の内容をスタックから戻す
     RET ; 呼び出し元に戻る
     END

; 基準日から指定された日付までの日数を計算するプログラム
DAYOFFST START
         RPUSH ; GR1〜7の内容をスタックに退避
         ; GR2から 年, 月, 日 をそれぞれ GR5, GR3, GR1 にロード
         LD GR5,0,GR2 ; GR5 = GR2[0]
         LD GR3,1,GR2 ; GR5 = GR2[1]
         LD GR1,2,GR2 ; GR5 = GR2[2]
         ; 1月1日からの日数を求める（平年）
         SUBL GR1,=1 ; 日 -= 1 | SUBL: 論理減算（unsigned sub）
         ; 1月1日から指定月の1日までの日数 = ACCMDAYS[月-1]
         LAD GR4,ACCMDAYS,GR3 ; アドレス ACCDAYS + GR3 を GR4 にロード
         ADDL GR1,-1,GR4 ; GR1 += *(GR4-1) | ADDL: 論理加算（unsigned add）
         ; 3月以降ならうるう年を考慮
         CPA GR3,=3 ; 算術比較 signed GR3 - 3 => FLAG
         JMI SKIP; FLAG < 0 なら SKIP にjump
         LD GR2,GR5 ; GR2（引数）に GR5（年）をセット
         CALL LEAPYEAR ; LEAPYEAR 呼び出し => GR0
         ADDL GR1,GR0 ; うるう年なら unsigned 日 += 1
         ; 1970年〜(年-1)年までの日数を加算
SKIP     LD GR2,=1970 ; GR2（引数）に 1970 セット
LOOP     CPA GR2,GR5 ; signed GR2 - GR5（年） => FLAG
         JZE BREAK ; FLAG == 0 なら BREAK にjump
         CALL LEAPYEAR ; LEAPYEAR 呼び出し => GR0
         ADDL GR0,365 ; unsigned GR0 += 365
         ADDL GR1,GR0 ; unsigned 日 += GR0
         ADDA GR2,=1 ; ADDA: 算術加算 | signed GR2 += 1
         JUMP LOOP ; LOOP にjump
BREAK    LD GR0,GR1 ; 戻り値 = GR1（日）
         RPOP ; GR1〜7の内容をスタックから戻す
         RET ; 呼び出し元に戻る
         END

; 平年の1月1日〜各月1日までの日数
; LABEL DC 定数 END: LABEL = 定数
ACCMDAYS DC 0,31,59,90,120,151,181,212,243,273,304,334
         END

; うるう年なら1を返すプログラム
LEAPYEAR START
         RPUSH ; GR1〜7の内容をスタックに退避
         LD GR0,=0 ; GR0 に戻り値 0（平年）を代入
         LD GR3,GR2 ; GR3 = GR2(年)
         ; GR3が4で割り切れないならプログラム終了
         ;  4で割り切れる数は下2桁が 00 のはず
         ;  => 11 との論理積をとったとき 0 なら4で割り切れる 
         AND GR3,=3 ; GR3 AND 3 => GR3
         JNZ FIN ; GR3 != 0（GR3が4で割り切れない）なら FIN にjump
         ; GR2が100で割り切れるか確認
         LD GR3,=100 ; GR3 = 100
         CALL DIVISL ; GR2がGR3で割り切れる? => GR0
         ; GR0(戻り値)が0（割り切れない）なら GR0 を 1（うるう年）に反転してプログラム終了
         XOR GR0,=1 ; GR0 を反転 => GR0 
         JNZ FIN ; GR0 != 0 なら FIN にjump
         ; GR2が400で割り切れるか確認
         LD GR3,=400 ; GR3 = 400
         CALL DIVISL ; GR2がGR3で割り切れる? => GR0
         ; GR0(戻り値)が1（割り切れる）ならうるう年なので、GR0 はそのままで良い
FIN      RPOP ; GR1〜7の内容をスタックから戻す
         RET ; 呼び出し元に戻る
         END

; GR2 が GR3 で割り切れるか判定するプログラム
DIVISIBL START
         RPUSH ; GR1〜7の内容をスタックに退避
         LD GR0,=0 ; GR0 に戻り値 0（割り切れない）を代入
         ; (GR2 = GR2 - GR3) > 0 ならループ
LOOP     SUBA GR2, GR3 ; signed GR2 -= GR3
         JPL LOOP ; GR2 > 0 ならループ
         JMI FIN ; GR2 < 0 ならループを抜ける
         LD GR0,=1 ; GR2 = 0 なら GR0 に 1（割り切れる）を代入
FIN      RPOP ; GR1〜7の内容をスタックから戻す
         RET ; 呼び出し元に戻る
         END
```
