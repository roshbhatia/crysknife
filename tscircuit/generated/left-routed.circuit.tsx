import artwork from "../models/left-artwork"
export default () => (
<board solderMaskColor="white" silkscreenColor="black" outline={[{"x": -70.37452611586556, "y": -27.353298265809542}, {"x": -70.37649290487181, "y": 30.873490264316672}, {"x": -70.35709263280621, "y": 31.01143423744665}, {"x": -70.30038838691242, "y": 31.138672355592625}, {"x": -70.21078152930814, "y": 31.245328444410852}, {"x": -70.0952273103771, "y": 31.323123898641505}, {"x": -69.9626950048718, "y": 31.36602026456177}, {"x": -30.790305003619295, "y": 38.222167824520014}, {"x": -30.657775712358898, "y": 38.26506268859194}, {"x": -30.54222346623223, "y": 38.34285509466518}, {"x": -30.452616953933216, "y": 38.44950711284201}, {"x": -30.395911069906248, "y": 38.57674084557157}, {"x": -30.376507095128147, "y": 38.714680926006174}, {"x": -30.376507095128147, "y": 42.85220172845368}, {"x": -30.362048185668982, "y": 42.97157436273343}, {"x": -30.319507747068116, "y": 43.084043011525175}, {"x": -30.251346128033333, "y": 43.183102991173634}, {"x": -30.161505491772033, "y": 43.2630251154795}, {"x": -30.055181818893487, "y": 43.31918704620672}, {"x": -29.938524395128155, "y": 43.34834062845368}, {"x": -10.814489750512735, "y": 45.738844971530604}, {"x": -10.697832371362352, "y": 45.76799856070047}, {"x": -10.591508698483239, "y": 45.824160491427534}, {"x": -10.501668062221313, "y": 45.9040826157333}, {"x": -10.43350644318582, "y": 46.003142595381746}, {"x": -10.39096600458413, "y": 46.11561124417362}, {"x": -10.376507095128147, "y": 46.234983878453676}, {"x": -10.376507095128147, "y": 47.66359280345368}, {"x": -10.359470014910556, "y": 47.79300232912743}, {"x": -10.309519806676576, "y": 47.913592810240004}, {"x": -10.230060495128129, "y": 48.017146203452526}, {"x": -10.126507101914996, "y": 48.096605515000164}, {"x": -10.005916620802026, "y": 48.1465557232332}, {"x": -9.876507095128147, "y": 48.16359280345368}, {"x": 8.073492904871841, "y": 48.16359280345368}, {"x": 8.202902430546715, "y": 48.146555723243495}, {"x": 8.323492911660082, "y": 48.09660551500831}, {"x": 8.42704630487296, "y": 48.01714620345834}, {"x": 8.506505616420412, "y": 47.91359281024354}, {"x": 8.556455824652687, "y": 47.79300232912896}, {"x": 8.573492904871841, "y": 47.66359280345368}, {"x": 8.573492904871841, "y": 46.234983878453676}, {"x": 8.587951776286673, "y": 46.115611227888394}, {"x": 8.630492196699748, "y": 46.0031425598219}, {"x": 8.698653815762981, "y": 45.904082566119854}, {"x": 8.788494465967062, "y": 45.82416044004402}, {"x": 8.894818160228311, "y": 45.767998524975084}, {"x": 9.011475604871833, "y": 45.73884497845368}, {"x": 28.135510249487254, "y": 43.34834063537675}, {"x": 28.252167649517673, "y": 43.31918708194035}, {"x": 28.358491343779832, "y": 43.263025166870264}, {"x": 28.448331993984226, "y": 43.18310304079281}, {"x": 28.51649361304709, "y": 43.08404304708889}, {"x": 28.55903403345897, "y": 42.97157437902054}, {"x": 28.57349290487184, "y": 42.85220172845368}, {"x": 28.57349290487184, "y": 41.17332586410368}, {"x": 28.591076550718952, "y": 41.04189349590125}, {"x": 28.64259076676973, "y": 40.91970537226702}, {"x": 28.72441231971709, "y": 40.81535554962292}, {"x": 28.830786320938188, "y": 40.73618343409736}, {"x": 28.954230994454036, "y": 40.68775756711346}, {"x": 29.08606390487185, "y": 40.67348396410368}, {"x": 48.07225672792768, "y": 41.15098671360354}, {"x": 48.20227931601113, "y": 41.13715416484755}, {"x": 48.324269526748054, "y": 41.09008398716031}, {"x": 48.42988458623458, "y": 41.01299525677246}, {"x": 48.511901599911596, "y": 40.91115998483461}, {"x": 48.56471151690397, "y": 40.79154257050707}, {"x": 48.58470272667091, "y": 40.662323513571934}, {"x": 48.61556145695988, "y": 39.28241415347958}, {"x": 48.634968534239135, "y": 39.155207368342204}, {"x": 48.68619831908708, "y": 39.037166285264306}, {"x": 48.76585772244121, "y": 38.93610903610802}, {"x": 48.868670685422444, "y": 38.85872891726094}, {"x": 48.9878276259428, "y": 38.81015102439182}, {"x": 49.115436455842314, "y": 38.79359280345426}, {"x": 69.87649290487184, "y": 38.79359280345368}, {"x": 70.00590243054967, "y": 38.77655572325636}, {"x": 70.12649291166588, "y": 38.726605515021056}, {"x": 70.23004630488049, "y": 38.647146203469}, {"x": 70.30950561642783, "y": 38.543592810250765}, {"x": 70.35945582465763, "y": 38.42300232913229}, {"x": 70.37649290487184, "y": 38.29359280345368}, {"x": 70.37649290487184, "y": -24.73343260267586}, {"x": 70.35945579998284, "y": -24.8628421207776}, {"x": 70.30950560487184, "y": -24.98343260267586}, {"x": 70.06149290487184, "y": -25.413003196546327}, {"x": 55.5142266419831, "y": -47.93494893200267}, {"x": 55.43277281361969, "y": -48.031607294944536}, {"x": 55.32968219014086, "y": -48.10475015584029}, {"x": 55.2115432933644, "y": -48.149702973524086}, {"x": 55.08590640636936, "y": -48.16359280345367}, {"x": 54.96080101045172, "y": -48.14553194351953}, {"x": 54.844222619194795, "y": -48.09667466728331}, {"x": 38.829439036402505, "y": -38.850535055102}, {"x": 38.73960144500228, "y": -38.809893858006575}, {"x": 38.643535136402534, "y": -38.78767305510202}, {"x": -0.20973222018534443, "y": -33.76554947767066}, {"x": -0.3258351567101272, "y": -33.73607401093899}, {"x": -0.43159562171345556, "y": -33.67982976963694}, {"x": -0.5209435138285983, "y": -33.60004477849232}, {"x": -11.507911537822281, "y": -21.118615441531816}, {"x": -11.597979376227244, "y": -21.038329440276044}, {"x": -11.704657381610474, "y": -20.981956843470897}, {"x": -11.821733428053108, "y": -20.952780382882622}, {"x": -11.942389913024186, "y": -20.952499069702966}, {"x": -69.81535512174105, "y": -27.849767766736235}, {"x": -69.9556379618916, "y": -27.846658360030304}, {"x": -70.08953278829395, "y": -27.80469265072483}, {"x": -70.20649459775431, "y": -27.72717568211418}, {"x": -70.2973119666482, "y": -27.620212366898073}, {"x": -70.35483249829842, "y": -27.492226689052856}]} layers={2} thickness={1.6} autorouter="auto-local" routingDisabled={false} placementDrcChecksDisabled={true} minTraceWidth={0.25} minTraceToPadEdgeClearance={0.2} minViaEdgeToPadEdgeClearance={0.25} minTraceToHoleEdgeClearance={0.3} minBoardEdgeClearance={0.55} minViaHoleDiameter={0.3} minViaPadDiameter={0.6}>
<chip name="P1" pcbX={-68.07150709512815} pcbY={-15.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P2" pcbX={-55.14450709512816} pcbY={-13.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P3" pcbX={-68.07150709512815} pcbY={4.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P4" pcbX={-55.14450709512816} pcbY={6.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P5" pcbX={-68.07150709512815} pcbY={24.348592803453677} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P6" pcbX={-55.14450709512816} pcbY={26.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P7" pcbX={-48.071507095128155} pcbY={-15.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P8" pcbX={-35.14450709512816} pcbY={-13.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P9" pcbX={-48.071507095128155} pcbY={4.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P10" pcbX={-35.14450709512816} pcbY={6.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P11" pcbX={-48.071507095128155} pcbY={24.348592803453677} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P12" pcbX={-35.14450709512816} pcbY={26.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P13" pcbX={-28.07150709512817} pcbY={-3.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P14" pcbX={-15.144507095128148} pcbY={-1.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P15" pcbX={-28.07150709512817} pcbY={16.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P16" pcbX={-15.144507095128148} pcbY={18.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P17" pcbX={-28.07150709512817} pcbY={36.34859280345368} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P18" pcbX={-15.144507095128148} pcbY={38.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P19" pcbX={-8.071507095128169} pcbY={1.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P20" pcbX={4.855492904871852} pcbY={3.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P21" pcbX={-8.071507095128169} pcbY={21.348592803453677} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P22" pcbX={4.855492904871852} pcbY={23.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P23" pcbX={-8.071507095128169} pcbY={41.34859280345368} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P24" pcbX={4.855492904871852} pcbY={43.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P25" pcbX={11.928492904871831} pcbY={-3.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P26" pcbX={24.855492904871852} pcbY={-1.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P27" pcbX={11.928492904871831} pcbY={16.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P28" pcbX={24.855492904871852} pcbY={18.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P29" pcbX={11.928492904871831} pcbY={36.34859280345368} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P30" pcbX={24.855492904871852} pcbY={38.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P31" pcbX={31.92849290487183} pcbY={-5.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P32" pcbX={44.85549290487185} pcbY={-3.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P33" pcbX={31.92849290487183} pcbY={14.348592803453684} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P34" pcbX={44.85549290487185} pcbY={16.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P35" pcbX={31.92849290487183} pcbY={34.34859280345368} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P36" pcbX={44.85549290487185} pcbY={36.888592803453676} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P37" pcbX={1.9284929048718311} pcbY={-21.651407196546316} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P38" pcbX={14.855492904871852} pcbY={-19.111407196546324} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P39" pcbX={24.827308800174194} pcbY={-22.65422266322072} layer="bottom" pcbRotation={-15.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P40" pcbX={37.971232331173354} pcbY={-23.54652486048677} layer="bottom" pcbRotation={-15.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P41" pcbX={48.48402007925938} pcbY={-35.83017388235908} layer="bottom" pcbRotation={60.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P42" pcbX={52.74781555364689} pcbY={-23.365063487637627} layer="bottom" pcbRotation={60.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P43" pcbX={-53.586507095128155} pcbY={-18.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P44" pcbX={-53.586507095128155} pcbY={-15.216407196546314} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P45" pcbX={-53.586507095128155} pcbY={1.483592803453675} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P46" pcbX={-53.586507095128155} pcbY={4.783592803453686} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P47" pcbX={-53.586507095128155} pcbY={21.483592803453682} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P48" pcbX={-53.586507095128155} pcbY={24.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P49" pcbX={-33.586507095128155} pcbY={-18.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P50" pcbX={-33.586507095128155} pcbY={-15.216407196546314} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P51" pcbX={-33.586507095128155} pcbY={1.483592803453675} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P52" pcbX={-33.586507095128155} pcbY={4.783592803453686} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P53" pcbX={-33.586507095128155} pcbY={21.483592803453682} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P54" pcbX={-33.586507095128155} pcbY={24.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P55" pcbX={-13.586507095128155} pcbY={-6.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P56" pcbX={-13.586507095128155} pcbY={-3.2164071965463137} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P57" pcbX={-13.586507095128155} pcbY={13.483592803453675} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P58" pcbX={-13.586507095128155} pcbY={16.783592803453686} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P59" pcbX={-13.586507095128155} pcbY={33.48359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P60" pcbX={-13.586507095128155} pcbY={36.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P61" pcbX={6.413492904871845} pcbY={-1.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P62" pcbX={6.413492904871845} pcbY={1.7835928034536863} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P63" pcbX={6.413492904871845} pcbY={18.483592803453682} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P64" pcbX={6.413492904871845} pcbY={21.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P65" pcbX={6.413492904871845} pcbY={38.48359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P66" pcbX={6.413492904871845} pcbY={41.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P67" pcbX={26.413492904871845} pcbY={-6.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P68" pcbX={26.413492904871845} pcbY={-3.2164071965463137} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P69" pcbX={26.413492904871845} pcbY={13.483592803453675} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P70" pcbX={26.413492904871845} pcbY={16.783592803453686} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P71" pcbX={26.413492904871845} pcbY={33.48359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P72" pcbX={26.413492904871845} pcbY={36.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P73" pcbX={46.413492904871845} pcbY={-8.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P74" pcbX={46.413492904871845} pcbY={-5.216407196546314} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P75" pcbX={46.413492904871845} pcbY={11.483592803453675} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P76" pcbX={46.413492904871845} pcbY={14.783592803453686} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P77" pcbX={46.413492904871845} pcbY={31.483592803453682} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P78" pcbX={46.413492904871845} pcbY={34.78359280345368} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P79" pcbX={16.413492904871845} pcbY={-24.516407196546325} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P80" pcbX={16.413492904871845} pcbY={-21.216407196546314} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P81" pcbX={38.07722778045269} pcbY={-29.170594009923278} layer="bottom" pcbRotation={75.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P82" pcbX={38.93133062929098} pcbY={-25.983038783169363} layer="bottom" pcbRotation={75.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P83" pcbX={58.20768282111618} pcbY={-24.718295896546323} layer="bottom" pcbRotation={150.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P84" pcbX={55.349798988627526} pcbY={-23.068295896546317} layer="bottom" pcbRotation={150.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P85" pcbX={51.09749290487184} pcbY={33.638592803453676} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P86" pcbX={51.09749290487184} pcbY={31.098592803453677} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P87" pcbX={51.09749290487184} pcbY={28.558592803453678} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P88" pcbX={51.09749290487184} pcbY={26.01859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P89" pcbX={51.09749290487184} pcbY={23.47859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P90" pcbX={51.09749290487184} pcbY={20.93859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P91" pcbX={51.09749290487184} pcbY={18.398592803453674} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P92" pcbX={51.09749290487184} pcbY={15.858592803453675} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P93" pcbX={51.09749290487184} pcbY={13.318592803453683} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P94" pcbX={51.09749290487184} pcbY={10.778592803453677} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P95" pcbX={51.09749290487184} pcbY={8.238592803453685} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P96" pcbX={51.09749290487184} pcbY={5.698592803453678} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P97" pcbX={66.33749290487185} pcbY={33.638592803453676} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P98" pcbX={66.33749290487185} pcbY={31.098592803453677} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P99" pcbX={66.33749290487185} pcbY={28.558592803453678} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P100" pcbX={66.33749290487185} pcbY={26.01859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P101" pcbX={66.33749290487185} pcbY={23.47859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P102" pcbX={66.33749290487185} pcbY={20.93859280345368} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P103" pcbX={66.33749290487185} pcbY={18.398592803453674} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P104" pcbX={66.33749290487185} pcbY={15.858592803453675} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P105" pcbX={66.33749290487185} pcbY={13.318592803453683} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P106" pcbX={66.33749290487185} pcbY={10.778592803453677} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P107" pcbX={66.33749290487185} pcbY={8.238592803453685} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P108" pcbX={66.33749290487185} pcbY={5.698592803453678} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P109" pcbX={69.38849290487184} pcbY={-3.5414071965463165} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P110" pcbX={67.17849290487183} pcbY={-3.5414071965463165} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P111" pcbX={67.17849290487183} pcbY={-10.841407196546328} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P112" pcbX={69.38849290487184} pcbY={-10.841407196546328} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P113" pcbX={66.52849290487183} pcbY={-9.441407196546322} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P114" pcbX={66.52849290487183} pcbY={-6.441407196546322} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P115" pcbX={66.52849290487183} pcbY={-4.941407196546322} layer="top" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P116" pcbX={61.34249290487185} pcbY={37.35859280345368} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P117" pcbX={61.34249290487185} pcbY={35.65859280345368} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P118" pcbX={56.09249290487185} pcbY={37.35859280345368} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P119" pcbX={56.09249290487185} pcbY={35.65859280345368} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P120" pcbX={56.26349290487184} pcbY={-4.941407196546322} layer="top" pcbRotation={90.0} footprint={<footprint><platedhole shape="circular_hole_with_rect_pad" rectPadWidth={1.2} rectPadHeight={1.75} rectBorderRadius={0.24} holeDiameter={0.75} holeOffsetX={0} holeOffsetY={0} portHints={["1"]} /></footprint>} />
<chip name="P121" pcbX={56.26349290487184} pcbY={-6.941407196546322} layer="top" pcbRotation={90.0} footprint={<footprint><platedhole shape="oval" outerWidth={1.2} outerHeight={1.75} holeWidth={0.75} holeHeight={0.75} portHints={["1"]} /></footprint>} />
<hole pcbX={-60.98650709512816} pcbY={-18.191407196546322} diameter={4.1} />
<hole pcbX={-55.90650709512816} pcbY={-18.191407196546322} diameter={1.9} />
<hole pcbX={-66.06650709512816} pcbY={-18.191407196546322} diameter={1.9} />
<hole pcbX={-58.446507095128155} pcbY={-13.111407196546324} diameter={3.0} />
<hole pcbX={-64.79650709512816} pcbY={-15.651407196546316} diameter={3.0} />
<hole pcbX={-60.98650709512816} pcbY={1.8085928034536778} diameter={4.1} />
<hole pcbX={-55.90650709512816} pcbY={1.8085928034536778} diameter={1.9} />
<hole pcbX={-66.06650709512816} pcbY={1.8085928034536778} diameter={1.9} />
<hole pcbX={-58.446507095128155} pcbY={6.888592803453676} diameter={3.0} />
<hole pcbX={-64.79650709512816} pcbY={4.348592803453684} diameter={3.0} />
<hole pcbX={-60.98650709512816} pcbY={21.808592803453678} diameter={4.1} />
<hole pcbX={-55.90650709512816} pcbY={21.808592803453678} diameter={1.9} />
<hole pcbX={-66.06650709512816} pcbY={21.808592803453678} diameter={1.9} />
<hole pcbX={-58.446507095128155} pcbY={26.888592803453676} diameter={3.0} />
<hole pcbX={-64.79650709512816} pcbY={24.348592803453677} diameter={3.0} />
<hole pcbX={-40.98650709512816} pcbY={-18.191407196546322} diameter={4.1} />
<hole pcbX={-35.90650709512816} pcbY={-18.191407196546322} diameter={1.9} />
<hole pcbX={-46.06650709512816} pcbY={-18.191407196546322} diameter={1.9} />
<hole pcbX={-38.446507095128155} pcbY={-13.111407196546324} diameter={3.0} />
<hole pcbX={-44.79650709512816} pcbY={-15.651407196546316} diameter={3.0} />
<hole pcbX={-40.98650709512816} pcbY={1.8085928034536778} diameter={4.1} />
<hole pcbX={-35.90650709512816} pcbY={1.8085928034536778} diameter={1.9} />
<hole pcbX={-46.06650709512816} pcbY={1.8085928034536778} diameter={1.9} />
<hole pcbX={-38.446507095128155} pcbY={6.888592803453676} diameter={3.0} />
<hole pcbX={-44.79650709512816} pcbY={4.348592803453684} diameter={3.0} />
<hole pcbX={-40.98650709512816} pcbY={21.808592803453678} diameter={4.1} />
<hole pcbX={-35.90650709512816} pcbY={21.808592803453678} diameter={1.9} />
<hole pcbX={-46.06650709512816} pcbY={21.808592803453678} diameter={1.9} />
<hole pcbX={-38.446507095128155} pcbY={26.888592803453676} diameter={3.0} />
<hole pcbX={-44.79650709512816} pcbY={24.348592803453677} diameter={3.0} />
<hole pcbX={-20.98650709512816} pcbY={-6.191407196546322} diameter={4.1} />
<hole pcbX={-15.906507095128148} pcbY={-6.191407196546322} diameter={1.9} />
<hole pcbX={-26.066507095128173} pcbY={-6.191407196546322} diameter={1.9} />
<hole pcbX={-18.44650709512817} pcbY={-1.111407196546324} diameter={3.0} />
<hole pcbX={-24.796507095128163} pcbY={-3.651407196546316} diameter={3.0} />
<hole pcbX={-20.98650709512816} pcbY={13.808592803453678} diameter={4.1} />
<hole pcbX={-15.906507095128148} pcbY={13.808592803453678} diameter={1.9} />
<hole pcbX={-26.066507095128173} pcbY={13.808592803453678} diameter={1.9} />
<hole pcbX={-18.44650709512817} pcbY={18.888592803453676} diameter={3.0} />
<hole pcbX={-24.796507095128163} pcbY={16.348592803453684} diameter={3.0} />
<hole pcbX={-20.98650709512816} pcbY={33.80859280345368} diameter={4.1} />
<hole pcbX={-15.906507095128148} pcbY={33.80859280345368} diameter={1.9} />
<hole pcbX={-26.066507095128173} pcbY={33.80859280345368} diameter={1.9} />
<hole pcbX={-18.44650709512817} pcbY={38.888592803453676} diameter={3.0} />
<hole pcbX={-24.796507095128163} pcbY={36.34859280345368} diameter={3.0} />
<hole pcbX={-0.9865070951281609} pcbY={-1.1914071965463222} diameter={4.1} />
<hole pcbX={4.093492904871852} pcbY={-1.1914071965463222} diameter={1.9} />
<hole pcbX={-6.066507095128173} pcbY={-1.1914071965463222} diameter={1.9} />
<hole pcbX={1.5534929048718311} pcbY={3.888592803453676} diameter={3.0} />
<hole pcbX={-4.796507095128163} pcbY={1.348592803453684} diameter={3.0} />
<hole pcbX={-0.9865070951281609} pcbY={18.808592803453678} diameter={4.1} />
<hole pcbX={4.093492904871852} pcbY={18.808592803453678} diameter={1.9} />
<hole pcbX={-6.066507095128173} pcbY={18.808592803453678} diameter={1.9} />
<hole pcbX={1.5534929048718311} pcbY={23.888592803453676} diameter={3.0} />
<hole pcbX={-4.796507095128163} pcbY={21.348592803453677} diameter={3.0} />
<hole pcbX={-0.9865070951281609} pcbY={38.80859280345368} diameter={4.1} />
<hole pcbX={4.093492904871852} pcbY={38.80859280345368} diameter={1.9} />
<hole pcbX={-6.066507095128173} pcbY={38.80859280345368} diameter={1.9} />
<hole pcbX={1.5534929048718311} pcbY={43.888592803453676} diameter={3.0} />
<hole pcbX={-4.796507095128163} pcbY={41.34859280345368} diameter={3.0} />
<hole pcbX={19.01349290487184} pcbY={-6.191407196546322} diameter={4.1} />
<hole pcbX={24.09349290487185} pcbY={-6.191407196546322} diameter={1.9} />
<hole pcbX={13.933492904871827} pcbY={-6.191407196546322} diameter={1.9} />
<hole pcbX={21.55349290487183} pcbY={-1.111407196546324} diameter={3.0} />
<hole pcbX={15.203492904871837} pcbY={-3.651407196546316} diameter={3.0} />
<hole pcbX={19.01349290487184} pcbY={13.808592803453678} diameter={4.1} />
<hole pcbX={24.09349290487185} pcbY={13.808592803453678} diameter={1.9} />
<hole pcbX={13.933492904871827} pcbY={13.808592803453678} diameter={1.9} />
<hole pcbX={21.55349290487183} pcbY={18.888592803453676} diameter={3.0} />
<hole pcbX={15.203492904871837} pcbY={16.348592803453684} diameter={3.0} />
<hole pcbX={19.01349290487184} pcbY={33.80859280345368} diameter={4.1} />
<hole pcbX={24.09349290487185} pcbY={33.80859280345368} diameter={1.9} />
<hole pcbX={13.933492904871827} pcbY={33.80859280345368} diameter={1.9} />
<hole pcbX={21.55349290487183} pcbY={38.888592803453676} diameter={3.0} />
<hole pcbX={15.203492904871837} pcbY={36.34859280345368} diameter={3.0} />
<hole pcbX={39.01349290487184} pcbY={-8.191407196546322} diameter={4.1} />
<hole pcbX={44.09349290487185} pcbY={-8.191407196546322} diameter={1.9} />
<hole pcbX={33.93349290487183} pcbY={-8.191407196546322} diameter={1.9} />
<hole pcbX={41.55349290487183} pcbY={-3.111407196546324} diameter={3.0} />
<hole pcbX={35.20349290487184} pcbY={-5.651407196546316} diameter={3.0} />
<hole pcbX={39.01349290487184} pcbY={11.808592803453678} diameter={4.1} />
<hole pcbX={44.09349290487185} pcbY={11.808592803453678} diameter={1.9} />
<hole pcbX={33.93349290487183} pcbY={11.808592803453678} diameter={1.9} />
<hole pcbX={41.55349290487183} pcbY={16.888592803453676} diameter={3.0} />
<hole pcbX={35.20349290487184} pcbY={14.348592803453684} diameter={3.0} />
<hole pcbX={39.01349290487184} pcbY={31.808592803453678} diameter={4.1} />
<hole pcbX={44.09349290487185} pcbY={31.808592803453678} diameter={1.9} />
<hole pcbX={33.93349290487183} pcbY={31.808592803453678} diameter={1.9} />
<hole pcbX={41.55349290487183} pcbY={36.888592803453676} diameter={3.0} />
<hole pcbX={35.20349290487184} pcbY={34.34859280345368} diameter={3.0} />
<hole pcbX={9.013492904871839} pcbY={-24.191407196546322} diameter={4.1} />
<hole pcbX={14.093492904871852} pcbY={-24.191407196546322} diameter={1.9} />
<hole pcbX={3.9334929048718266} pcbY={-24.191407196546322} diameter={1.9} />
<hole pcbX={11.553492904871831} pcbY={-19.111407196546324} diameter={3.0} />
<hole pcbX={5.203492904871837} pcbY={-21.651407196546316} diameter={3.0} />
<hole pcbX={31.01349290487184} pcbY={-26.941407196546322} diameter={4.1} />
<hole pcbX={35.92039610242031} pcbY={-28.25620794566713} diameter={1.9} />
<hole pcbX={26.106589707323366} pcbY={-25.626606447425516} diameter={1.9} />
<hole pcbX={34.781745252766854} pcbY={-22.691904373558245} diameter={3.0} />
<hole pcbX={27.990715881270887} pcbY={-23.501855035931484} diameter={3.0} />
<hole pcbX={54.226224604871845} pcbY={-30.964383896546323} diameter={4.1} />
<hole pcbX={56.76622460487184} pcbY={-26.564974845321373} diameter={1.9} />
<hole pcbX={51.68622460487185} pcbY={-35.36379294777127} diameter={1.9} />
<hole pcbX={51.096815553646906} pcbY={-26.224679370933842} diameter={3.0} />
<hole pcbX={50.12152007925937} pcbY={-32.99394068496504} diameter={3.0} />
<hole pcbX={68.28849290487184} pcbY={-5.691407196546322} diameter={0.9} />
<hole pcbX={68.28849290487184} pcbY={-8.691407196546322} diameter={0.9} />
<hole pcbX={58.71749290487185} pcbY={37.88359280345368} diameter={0.75} />
<hole pcbX={58.71749290487185} pcbY={35.13359280345368} diameter={0.75} />
{artwork.map(([x, y, width, height, layer], index) => <silkscreenrect key={index} pcbX={x} pcbY={y} width={width} height={height} layer={layer} filled={true} stroke="none" strokeWidth={0} />)}
<net name="N0" connectsTo={[".P113 > .pin1", ".P121 > .pin1"]} />
<net name="N1" connectsTo={[".P1 > .pin1", ".P3 > .pin1", ".P5 > .pin1", ".P101 > .pin1"]} />
<net name="N2" connectsTo={[".P7 > .pin1", ".P9 > .pin1", ".P11 > .pin1", ".P102 > .pin1"]} />
<net name="N3" connectsTo={[".P13 > .pin1", ".P15 > .pin1", ".P17 > .pin1", ".P103 > .pin1"]} />
<net name="N4" connectsTo={[".P19 > .pin1", ".P21 > .pin1", ".P23 > .pin1", ".P37 > .pin1", ".P104 > .pin1"]} />
<net name="N5" connectsTo={[".P25 > .pin1", ".P27 > .pin1", ".P29 > .pin1", ".P39 > .pin1", ".P105 > .pin1"]} />
<net name="N6" connectsTo={[".P31 > .pin1", ".P33 > .pin1", ".P35 > .pin1", ".P41 > .pin1", ".P106 > .pin1"]} />
<net name="N7" connectsTo={[".P87 > .pin1", ".P88 > .pin1", ".P98 > .pin1", ".P116 > .pin1", ".P118 > .pin1", ".P120 > .pin1"]} />
<net name="N16" connectsTo={[".P47 > .pin1", ".P53 > .pin1", ".P59 > .pin1", ".P65 > .pin1", ".P71 > .pin1", ".P77 > .pin1", ".P92 > .pin1"]} />
<net name="N17" connectsTo={[".P45 > .pin1", ".P51 > .pin1", ".P57 > .pin1", ".P63 > .pin1", ".P69 > .pin1", ".P75 > .pin1", ".P93 > .pin1"]} />
<net name="N18" connectsTo={[".P43 > .pin1", ".P49 > .pin1", ".P55 > .pin1", ".P61 > .pin1", ".P67 > .pin1", ".P73 > .pin1", ".P94 > .pin1"]} />
<net name="N19" connectsTo={[".P79 > .pin1", ".P81 > .pin1", ".P83 > .pin1", ".P95 > .pin1"]} />
<net name="N20" connectsTo={[".P97 > .pin1", ".P114 > .pin1"]} />
<net name="N21" connectsTo={[".P99 > .pin1", ".P117 > .pin1", ".P119 > .pin1"]} />
<net name="N23" connectsTo={[".P42 > .pin1", ".P84 > .pin1"]} />
<net name="N24" connectsTo={[".P26 > .pin1", ".P68 > .pin1"]} />
<net name="N25" connectsTo={[".P28 > .pin1", ".P70 > .pin1"]} />
<net name="N26" connectsTo={[".P30 > .pin1", ".P72 > .pin1"]} />
<net name="N27" connectsTo={[".P32 > .pin1", ".P74 > .pin1"]} />
<net name="N28" connectsTo={[".P34 > .pin1", ".P76 > .pin1"]} />
<net name="N29" connectsTo={[".P36 > .pin1", ".P78 > .pin1"]} />
<net name="N30" connectsTo={[".P40 > .pin1", ".P82 > .pin1"]} />
<net name="N31" connectsTo={[".P20 > .pin1", ".P62 > .pin1"]} />
<net name="N32" connectsTo={[".P22 > .pin1", ".P64 > .pin1"]} />
<net name="N33" connectsTo={[".P24 > .pin1", ".P66 > .pin1"]} />
<net name="N34" connectsTo={[".P38 > .pin1", ".P80 > .pin1"]} />
<net name="N35" connectsTo={[".P2 > .pin1", ".P44 > .pin1"]} />
<net name="N36" connectsTo={[".P4 > .pin1", ".P46 > .pin1"]} />
<net name="N37" connectsTo={[".P6 > .pin1", ".P48 > .pin1"]} />
<net name="N38" connectsTo={[".P8 > .pin1", ".P50 > .pin1"]} />
<net name="N39" connectsTo={[".P10 > .pin1", ".P52 > .pin1"]} />
<net name="N40" connectsTo={[".P12 > .pin1", ".P54 > .pin1"]} />
<net name="N41" connectsTo={[".P14 > .pin1", ".P56 > .pin1"]} />
<net name="N42" connectsTo={[".P16 > .pin1", ".P58 > .pin1"]} />
<net name="N43" connectsTo={[".P18 > .pin1", ".P60 > .pin1"]} />
</board>
)
