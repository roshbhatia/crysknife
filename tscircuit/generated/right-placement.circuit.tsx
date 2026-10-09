import artwork from "../models/right-artwork"
export default () => (
<board solderMaskColor="white" silkscreenColor="black" outline={[{"x": 70.37452611586556, "y": -27.35329826581122}, {"x": 70.37649290487184, "y": 30.87349026617764}, {"x": 70.35709267018831, "y": 31.011434254674292}, {"x": 70.30038843763435, "y": 31.138672391238742}, {"x": 70.21078157270563, "y": 31.24532848878396}, {"x": 70.09522733333816, "y": 31.323123933060174}, {"x": 69.96269500487182, "y": 31.366020265025753}, {"x": 30.790305003619295, "y": 38.22216782451834}, {"x": 30.65777571236572, "y": 38.26506268861497}, {"x": 30.542223466237772, "y": 38.34285509467919}, {"x": 30.45261695393694, "y": 38.4495071128493}, {"x": 30.395911069908664, "y": 38.57674084557392}, {"x": 30.376507095128147, "y": 38.71468092600449}, {"x": 30.376507095128147, "y": 42.852201728452}, {"x": 30.36204822371414, "y": 42.97157437901772}, {"x": 30.31950780330149, "y": 43.08404304708472}, {"x": 30.251346184238287, "y": 43.183103040787195}, {"x": 30.16150553403395, "y": 43.26302516686323}, {"x": 30.055181839772246, "y": 43.31918708193203}, {"x": 29.938524395128155, "y": 43.348340628452}, {"x": 10.814489750512763, "y": 45.73884497152892}, {"x": 10.69783235048277, "y": 45.767998524967986}, {"x": 10.591508656220412, "y": 45.8241604400371}, {"x": 10.501668006015763, "y": 45.904082566113864}, {"x": 10.433506386952729, "y": 46.003142559817334}, {"x": 10.390965966540818, "y": 46.115611227885395}, {"x": 10.376507095128147, "y": 46.234983878452}, {"x": 10.376507095128147, "y": 47.663592803452005}, {"x": 10.359470014906236, "y": 47.79300232912555}, {"x": 10.309519806672597, "y": 47.9135928102381}, {"x": 10.230060495125116, "y": 48.01714620345116}, {"x": 10.126507101913234, "y": 48.09660551500019}, {"x": 10.005916620801429, "y": 48.14655572323561}, {"x": 9.876507095128147, "y": 48.163592803452005}, {"x": -8.073492904871841, "y": 48.163592803452005}, {"x": -8.202902430546573, "y": 48.146555723234314}, {"x": -8.323492911660537, "y": 48.09660551500245}, {"x": -8.427046304874068, "y": 48.017146203454566}, {"x": -8.50650561642172, "y": 47.91359281024084}, {"x": -8.556455824653312, "y": 47.79300232912677}, {"x": -8.573492904871841, "y": 47.663592803452005}, {"x": -8.573492904871841, "y": 46.234983878452}, {"x": -8.587951814328079, "y": 46.11561124417227}, {"x": -8.630492252930367, "y": 46.00314259538084}, {"x": -8.69865387196603, "y": 45.904082615732726}, {"x": -8.788494508227757, "y": 45.82416049142702}, {"x": -8.894818181106444, "y": 45.76799856069961}, {"x": -9.011475604871833, "y": 45.738844978452}, {"x": -28.135510249487226, "y": 43.348340635375074}, {"x": -28.25216762863792, "y": 43.31918704620576}, {"x": -28.35849130151729, "y": 43.263025115478925}, {"x": -28.44833193777933, "y": 43.18310299117312}, {"x": -28.516493556814765, "y": 43.08404301152444}, {"x": -28.55903399541603, "y": 42.97157436273228}, {"x": -28.57349290487184, "y": 42.852201728452}, {"x": -28.57349290487184, "y": 41.173325864102004}, {"x": -28.591076585416346, "y": 41.0418935125341}, {"x": -28.64259081708579, "y": 40.919705408383976}, {"x": -28.724412368460747, "y": 40.81535559961134}, {"x": -28.83078635577786, "y": 40.73618348531248}, {"x": -28.954231010210037, "y": 40.68775760222907}, {"x": -29.08606390487185, "y": 40.673483964102005}, {"x": -48.07225672792757, "y": 41.15098671360186}, {"x": -48.20227931526287, "y": 41.13715416314708}, {"x": -48.32426952509191, "y": 41.09008398467664}, {"x": -48.429884583914216, "y": 41.01299525433727}, {"x": -48.511901597511425, "y": 40.91115998306072}, {"x": -48.564711515243204, "y": 40.79154256967732}, {"x": -48.58470272667087, "y": 40.66232351357026}, {"x": -48.615561456959895, "y": 39.28241415347699}, {"x": -48.63496849961989, "y": 39.155207351370166}, {"x": -48.68619826882592, "y": 39.03716624890788}, {"x": -48.76585767355837, "y": 38.936108986125404}, {"x": -48.86867065019767, "y": 38.858728866210896}, {"x": -48.987827609750624, "y": 38.810150989420016}, {"x": -49.115436455842314, "y": 38.79359280345167}, {"x": -69.87649290487184, "y": 38.793592803452}, {"x": -70.00590243054647, "y": 38.77655572323312}, {"x": -70.12649291166032, "y": 38.72660551500081}, {"x": -70.23004630487408, "y": 38.64714620345311}, {"x": -70.30950561642258, "y": 38.543592810239964}, {"x": -70.35945582465583, "y": 38.423002329126504}, {"x": -70.37649290487184, "y": 38.293592803452}, {"x": -70.37649290487184, "y": -24.733432602677524}, {"x": -70.35945580001116, "y": -24.86284212078077}, {"x": -70.30950560487184, "y": -24.983432602677524}, {"x": -70.06149290487184, "y": -25.413003196548004}, {"x": -55.51422664198313, "y": -47.93494893200432}, {"x": -55.432772813612104, "y": -48.031607294939874}, {"x": -55.32968219013502, "y": -48.1047501558358}, {"x": -55.21154329336035, "y": -48.14970297352056}, {"x": -55.085906406366874, "y": -48.16359280345199}, {"x": -54.9608010104502, "y": -48.14553194352044}, {"x": -54.84422261919478, "y": -48.096674667285015}, {"x": -38.82943903640259, "y": -38.850535055103705}, {"x": -38.73960144500208, "y": -38.80989385801189}, {"x": -38.64353513640259, "y": -38.787673055103724}, {"x": 0.2097322201852876, "y": -33.76554947767234}, {"x": 0.32583515670302177, "y": -33.73607411093832}, {"x": 0.4315956216939867, "y": -33.6798298696193}, {"x": 0.5209435138285414, "y": -33.60004487849402}, {"x": 11.50791153782231, "y": -21.11861544153348}, {"x": 11.597979454359063, "y": -21.038329453591274}, {"x": 11.704657433873876, "y": -20.98195686173402}, {"x": 11.821733453266916, "y": -20.95278039674696}, {"x": 11.942389913024186, "y": -20.952499069704643}, {"x": 69.8153551217411, "y": -27.849767766737926}, {"x": 69.95563794918323, "y": -27.846658325752017}, {"x": 70.08953275798632, "y": -27.804692600235683}, {"x": 70.20649455367203, "y": -27.727175632464082}, {"x": 70.29731192010337, "y": -27.62021233082747}, {"x": 70.35483246576857, "y": -27.492226672377384}]} layers={2} thickness={1.6} autorouter="auto-local" routingDisabled={true} placementDrcChecksDisabled={false} minTraceWidth={0.25} minTraceToPadEdgeClearance={0.2} minViaEdgeToPadEdgeClearance={0.25} minTraceToHoleEdgeClearance={0.3} minBoardEdgeClearance={0.55} minViaHoleDiameter={0.3} minViaPadDiameter={0.6}>
<chip name="P1" pcbX={53.90150709512815} pcbY={-15.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P2" pcbX={66.82850709512817} pcbY={-13.111407196548} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P3" pcbX={53.90150709512815} pcbY={4.348592803452007} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P4" pcbX={66.82850709512817} pcbY={6.888592803451999} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P5" pcbX={53.90150709512815} pcbY={24.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P6" pcbX={66.82850709512817} pcbY={26.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P7" pcbX={33.90150709512815} pcbY={-15.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P8" pcbX={46.828507095128174} pcbY={-13.111407196548} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P9" pcbX={33.90150709512815} pcbY={4.348592803452007} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P10" pcbX={46.828507095128174} pcbY={6.888592803451999} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P11" pcbX={33.90150709512815} pcbY={24.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P12" pcbX={46.828507095128174} pcbY={26.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P13" pcbX={13.901507095128153} pcbY={-3.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P14" pcbX={26.828507095128174} pcbY={-1.1114071965480008} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P15" pcbX={13.901507095128153} pcbY={16.348592803452007} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P16" pcbX={26.828507095128174} pcbY={18.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P17" pcbX={13.901507095128153} pcbY={36.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P18" pcbX={26.828507095128174} pcbY={38.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P19" pcbX={-6.098492904871847} pcbY={1.3485928034520072} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P20" pcbX={6.828507095128174} pcbY={3.888592803451999} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P21" pcbX={-6.098492904871847} pcbY={21.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P22" pcbX={6.828507095128174} pcbY={23.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P23" pcbX={-6.098492904871847} pcbY={41.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P24" pcbX={6.828507095128174} pcbY={43.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P25" pcbX={-26.098492904871847} pcbY={-3.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P26" pcbX={-13.171492904871826} pcbY={-1.1114071965480008} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P27" pcbX={-26.098492904871847} pcbY={16.348592803452007} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P28" pcbX={-13.171492904871826} pcbY={18.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P29" pcbX={-26.098492904871847} pcbY={36.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P30" pcbX={-13.171492904871826} pcbY={38.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P31" pcbX={-46.09849290487183} pcbY={-5.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P32" pcbX={-33.171492904871826} pcbY={-3.111407196548001} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P33" pcbX={-46.09849290487183} pcbY={14.348592803452007} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P34" pcbX={-33.171492904871826} pcbY={16.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P35" pcbX={-46.09849290487183} pcbY={34.348592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P36" pcbX={-33.171492904871826} pcbY={36.888592803452} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P37" pcbX={-16.098492904871847} pcbY={-21.651407196547993} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P38" pcbX={-3.171492904871826} pcbY={-19.111407196548} layer="bottom" pcbRotation={0.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P39" pcbX={-38.514477758690305} pcbY={-26.321688532325126} layer="bottom" pcbRotation={15.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P40" pcbX={-26.685354976811908} pcbY={-20.522483137510605} layer="bottom" pcbRotation={15.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P41" pcbX={-55.569020079259374} pcbY={-23.558593910735254} layer="bottom" pcbRotation={-60.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P42" pcbX={-46.90581555364689} pcbY={-33.48370430545668} layer="bottom" pcbRotation={-60.0} footprint={<footprint><smtpad shape="rotated_rect" width={2.55} height={2.5} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P43" pcbX={68.38650709512817} pcbY={-18.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P44" pcbX={68.38650709512817} pcbY={-15.21640719654799} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P45" pcbX={68.38650709512817} pcbY={1.483592803451998} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P46" pcbX={68.38650709512817} pcbY={4.783592803452009} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P47" pcbX={68.38650709512817} pcbY={21.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P48" pcbX={68.38650709512817} pcbY={24.783592803452002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P49" pcbX={48.38650709512817} pcbY={-18.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P50" pcbX={48.38650709512817} pcbY={-15.21640719654799} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P51" pcbX={48.38650709512817} pcbY={1.483592803451998} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P52" pcbX={48.38650709512817} pcbY={4.783592803452009} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P53" pcbX={48.38650709512817} pcbY={21.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P54" pcbX={48.38650709512817} pcbY={24.783592803452002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P55" pcbX={28.386507095128167} pcbY={-6.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P56" pcbX={28.386507095128167} pcbY={-3.2164071965479906} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P57" pcbX={28.386507095128167} pcbY={13.483592803451998} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P58" pcbX={28.386507095128167} pcbY={16.78359280345201} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P59" pcbX={28.386507095128167} pcbY={33.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P60" pcbX={28.386507095128167} pcbY={36.783592803452} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P61" pcbX={8.386507095128167} pcbY={-1.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P62" pcbX={8.386507095128167} pcbY={1.7835928034520094} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P63" pcbX={8.386507095128167} pcbY={18.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P64" pcbX={8.386507095128167} pcbY={21.783592803452002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P65" pcbX={8.386507095128167} pcbY={38.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P66" pcbX={8.386507095128167} pcbY={41.783592803452} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P67" pcbX={-11.613492904871833} pcbY={-6.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P68" pcbX={-11.613492904871833} pcbY={-3.2164071965479906} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P69" pcbX={-11.613492904871833} pcbY={13.483592803451998} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P70" pcbX={-11.613492904871833} pcbY={16.78359280345201} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P71" pcbX={-11.613492904871833} pcbY={33.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P72" pcbX={-11.613492904871833} pcbY={36.783592803452} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P73" pcbX={-31.613492904871833} pcbY={-8.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P74" pcbX={-31.613492904871833} pcbY={-5.216407196547991} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P75" pcbX={-31.613492904871833} pcbY={11.483592803451998} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P76" pcbX={-31.613492904871833} pcbY={14.78359280345201} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P77" pcbX={-31.613492904871833} pcbY={31.483592803452005} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P78" pcbX={-31.613492904871833} pcbY={34.783592803452} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P79" pcbX={-1.6134929048718334} pcbY={-24.516407196548002} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P80" pcbX={-1.6134929048718334} pcbY={-21.21640719654799} layer="bottom" pcbRotation={90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P81" pcbX={-23.781525580452694} pcbY={-25.34007210992496} layer="bottom" pcbRotation={105.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P82" pcbX={-24.63562842929099} pcbY={-22.152516883171046} layer="bottom" pcbRotation={105.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P83" pcbX={-50.807682821116174} pcbY={-37.535471896548} layer="bottom" pcbRotation={30.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P84" pcbX={-47.94979898862752} pcbY={-35.885471896548} layer="bottom" pcbRotation={30.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.9} height={1.2} ccwRotation={0} layer="bottom" portHints={["1"]} /></footprint>} />
<chip name="P85" pcbX={-66.33749290487185} pcbY={33.638592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P86" pcbX={-66.33749290487185} pcbY={31.098592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P87" pcbX={-66.33749290487185} pcbY={28.558592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P88" pcbX={-66.33749290487185} pcbY={26.018592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P89" pcbX={-66.33749290487185} pcbY={23.478592803452003} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P90" pcbX={-66.33749290487185} pcbY={20.938592803452003} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P91" pcbX={-66.33749290487185} pcbY={18.398592803451997} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P92" pcbX={-66.33749290487185} pcbY={15.858592803451998} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P93" pcbX={-66.33749290487185} pcbY={13.318592803452006} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P94" pcbX={-66.33749290487185} pcbY={10.778592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P95" pcbX={-66.33749290487185} pcbY={8.238592803452008} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P96" pcbX={-66.33749290487185} pcbY={5.6985928034520015} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P97" pcbX={-51.09749290487184} pcbY={33.638592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P98" pcbX={-51.09749290487184} pcbY={31.098592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P99" pcbX={-51.09749290487184} pcbY={28.558592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P100" pcbX={-51.09749290487184} pcbY={26.018592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P101" pcbX={-51.09749290487184} pcbY={23.478592803452003} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P102" pcbX={-51.09749290487184} pcbY={20.938592803452003} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P103" pcbX={-51.09749290487184} pcbY={18.398592803451997} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P104" pcbX={-51.09749290487184} pcbY={15.858592803451998} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P105" pcbX={-51.09749290487184} pcbY={13.318592803452006} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P106" pcbX={-51.09749290487184} pcbY={10.778592803452} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P107" pcbX={-51.09749290487184} pcbY={8.238592803452008} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P108" pcbX={-51.09749290487184} pcbY={5.6985928034520015} layer="top" pcbRotation={0.0} footprint={<footprint><platedhole shape="circle" outerDiameter={1.7} holeDiameter={1.0} portHints={["1"]} /></footprint>} />
<chip name="P109" pcbX={-69.38849290487184} pcbY={-10.841407196548005} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P110" pcbX={-67.17849290487185} pcbY={-10.841407196548005} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P111" pcbX={-67.17849290487185} pcbY={-3.5414071965479934} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P112" pcbX={-69.38849290487184} pcbY={-3.5414071965479934} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.0} height={0.8} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P113" pcbX={-66.52849290487184} pcbY={-4.941407196547999} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P114" pcbX={-66.52849290487184} pcbY={-7.941407196547999} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P115" pcbX={-66.52849290487184} pcbY={-9.441407196547999} layer="top" pcbRotation={-90.0} footprint={<footprint><smtpad shape="rotated_rect" width={0.7} height={1.5} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P116" pcbX={-56.09249290487185} pcbY={37.358592803452005} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P117" pcbX={-56.09249290487185} pcbY={35.658592803452} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P118" pcbX={-61.34249290487185} pcbY={37.358592803452005} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P119" pcbX={-61.34249290487185} pcbY={35.658592803452} layer="top" pcbRotation={180.0} footprint={<footprint><smtpad shape="rotated_rect" width={1.55} height={1.0} ccwRotation={0} layer="top" portHints={["1"]} /></footprint>} />
<chip name="P120" pcbX={-56.26349290487184} pcbY={-4.941407196547999} layer="top" pcbRotation={90.0} footprint={<footprint><platedhole shape="circular_hole_with_rect_pad" rectPadWidth={1.2} rectPadHeight={1.75} rectBorderRadius={0.24} holeDiameter={0.75} holeOffsetX={0} holeOffsetY={0} portHints={["1"]} /></footprint>} />
<chip name="P121" pcbX={-56.26349290487184} pcbY={-6.941407196547999} layer="top" pcbRotation={90.0} footprint={<footprint><platedhole shape="oval" outerWidth={1.2} outerHeight={1.75} holeWidth={0.75} holeHeight={0.75} portHints={["1"]} /></footprint>} />
<hole pcbX={60.98650709512816} pcbY={-18.191407196548} diameter={4.1} />
<hole pcbX={66.06650709512817} pcbY={-18.191407196548} diameter={1.9} />
<hole pcbX={55.90650709512815} pcbY={-18.191407196548} diameter={1.9} />
<hole pcbX={63.52650709512815} pcbY={-13.111407196548} diameter={3.0} />
<hole pcbX={57.17650709512816} pcbY={-15.651407196547993} diameter={3.0} />
<hole pcbX={60.98650709512816} pcbY={1.808592803452001} diameter={4.1} />
<hole pcbX={66.06650709512817} pcbY={1.808592803452001} diameter={1.9} />
<hole pcbX={55.90650709512815} pcbY={1.808592803452001} diameter={1.9} />
<hole pcbX={63.52650709512815} pcbY={6.888592803451999} diameter={3.0} />
<hole pcbX={57.17650709512816} pcbY={4.348592803452007} diameter={3.0} />
<hole pcbX={60.98650709512816} pcbY={21.808592803452} diameter={4.1} />
<hole pcbX={66.06650709512817} pcbY={21.808592803452} diameter={1.9} />
<hole pcbX={55.90650709512815} pcbY={21.808592803452} diameter={1.9} />
<hole pcbX={63.52650709512815} pcbY={26.888592803452} diameter={3.0} />
<hole pcbX={57.17650709512816} pcbY={24.348592803452} diameter={3.0} />
<hole pcbX={40.98650709512816} pcbY={-18.191407196548} diameter={4.1} />
<hole pcbX={46.06650709512817} pcbY={-18.191407196548} diameter={1.9} />
<hole pcbX={35.90650709512815} pcbY={-18.191407196548} diameter={1.9} />
<hole pcbX={43.52650709512815} pcbY={-13.111407196548} diameter={3.0} />
<hole pcbX={37.17650709512816} pcbY={-15.651407196547993} diameter={3.0} />
<hole pcbX={40.98650709512816} pcbY={1.808592803452001} diameter={4.1} />
<hole pcbX={46.06650709512817} pcbY={1.808592803452001} diameter={1.9} />
<hole pcbX={35.90650709512815} pcbY={1.808592803452001} diameter={1.9} />
<hole pcbX={43.52650709512815} pcbY={6.888592803451999} diameter={3.0} />
<hole pcbX={37.17650709512816} pcbY={4.348592803452007} diameter={3.0} />
<hole pcbX={40.98650709512816} pcbY={21.808592803452} diameter={4.1} />
<hole pcbX={46.06650709512817} pcbY={21.808592803452} diameter={1.9} />
<hole pcbX={35.90650709512815} pcbY={21.808592803452} diameter={1.9} />
<hole pcbX={43.52650709512815} pcbY={26.888592803452} diameter={3.0} />
<hole pcbX={37.17650709512816} pcbY={24.348592803452} diameter={3.0} />
<hole pcbX={20.98650709512816} pcbY={-6.191407196547999} diameter={4.1} />
<hole pcbX={26.066507095128173} pcbY={-6.191407196547999} diameter={1.9} />
<hole pcbX={15.906507095128148} pcbY={-6.191407196547999} diameter={1.9} />
<hole pcbX={23.526507095128153} pcbY={-1.1114071965480008} diameter={3.0} />
<hole pcbX={17.17650709512816} pcbY={-3.651407196547993} diameter={3.0} />
<hole pcbX={20.98650709512816} pcbY={13.808592803452001} diameter={4.1} />
<hole pcbX={26.066507095128173} pcbY={13.808592803452001} diameter={1.9} />
<hole pcbX={15.906507095128148} pcbY={13.808592803452001} diameter={1.9} />
<hole pcbX={23.526507095128153} pcbY={18.888592803452} diameter={3.0} />
<hole pcbX={17.17650709512816} pcbY={16.348592803452007} diameter={3.0} />
<hole pcbX={20.98650709512816} pcbY={33.808592803452} diameter={4.1} />
<hole pcbX={26.066507095128173} pcbY={33.808592803452} diameter={1.9} />
<hole pcbX={15.906507095128148} pcbY={33.808592803452} diameter={1.9} />
<hole pcbX={23.526507095128153} pcbY={38.888592803452} diameter={3.0} />
<hole pcbX={17.17650709512816} pcbY={36.348592803452} diameter={3.0} />
<hole pcbX={0.9865070951281609} pcbY={-1.191407196547999} diameter={4.1} />
<hole pcbX={6.066507095128173} pcbY={-1.191407196547999} diameter={1.9} />
<hole pcbX={-4.093492904871852} pcbY={-1.191407196547999} diameter={1.9} />
<hole pcbX={3.526507095128153} pcbY={3.888592803451999} diameter={3.0} />
<hole pcbX={-2.8234929048718413} pcbY={1.3485928034520072} diameter={3.0} />
<hole pcbX={0.9865070951281609} pcbY={18.808592803452} diameter={4.1} />
<hole pcbX={6.066507095128173} pcbY={18.808592803452} diameter={1.9} />
<hole pcbX={-4.093492904871852} pcbY={18.808592803452} diameter={1.9} />
<hole pcbX={3.526507095128153} pcbY={23.888592803452} diameter={3.0} />
<hole pcbX={-2.8234929048718413} pcbY={21.348592803452} diameter={3.0} />
<hole pcbX={0.9865070951281609} pcbY={38.808592803452} diameter={4.1} />
<hole pcbX={6.066507095128173} pcbY={38.808592803452} diameter={1.9} />
<hole pcbX={-4.093492904871852} pcbY={38.808592803452} diameter={1.9} />
<hole pcbX={3.526507095128153} pcbY={43.888592803452} diameter={3.0} />
<hole pcbX={-2.8234929048718413} pcbY={41.348592803452} diameter={3.0} />
<hole pcbX={-19.01349290487184} pcbY={-6.191407196547999} diameter={4.1} />
<hole pcbX={-13.933492904871827} pcbY={-6.191407196547999} diameter={1.9} />
<hole pcbX={-24.09349290487185} pcbY={-6.191407196547999} diameter={1.9} />
<hole pcbX={-16.473492904871847} pcbY={-1.1114071965480008} diameter={3.0} />
<hole pcbX={-22.82349290487184} pcbY={-3.651407196547993} diameter={3.0} />
<hole pcbX={-19.01349290487184} pcbY={13.808592803452001} diameter={4.1} />
<hole pcbX={-13.933492904871827} pcbY={13.808592803452001} diameter={1.9} />
<hole pcbX={-24.09349290487185} pcbY={13.808592803452001} diameter={1.9} />
<hole pcbX={-16.473492904871847} pcbY={18.888592803452} diameter={3.0} />
<hole pcbX={-22.82349290487184} pcbY={16.348592803452007} diameter={3.0} />
<hole pcbX={-19.01349290487184} pcbY={33.808592803452} diameter={4.1} />
<hole pcbX={-13.933492904871827} pcbY={33.808592803452} diameter={1.9} />
<hole pcbX={-24.09349290487185} pcbY={33.808592803452} diameter={1.9} />
<hole pcbX={-16.473492904871847} pcbY={38.888592803452} diameter={3.0} />
<hole pcbX={-22.82349290487184} pcbY={36.348592803452} diameter={3.0} />
<hole pcbX={-39.01349290487184} pcbY={-8.191407196547999} diameter={4.1} />
<hole pcbX={-33.93349290487183} pcbY={-8.191407196547999} diameter={1.9} />
<hole pcbX={-44.09349290487185} pcbY={-8.191407196547999} diameter={1.9} />
<hole pcbX={-36.47349290487185} pcbY={-3.111407196548001} diameter={3.0} />
<hole pcbX={-42.82349290487184} pcbY={-5.651407196547993} diameter={3.0} />
<hole pcbX={-39.01349290487184} pcbY={11.808592803452001} diameter={4.1} />
<hole pcbX={-33.93349290487183} pcbY={11.808592803452001} diameter={1.9} />
<hole pcbX={-44.09349290487185} pcbY={11.808592803452001} diameter={1.9} />
<hole pcbX={-36.47349290487185} pcbY={16.888592803452} diameter={3.0} />
<hole pcbX={-42.82349290487184} pcbY={14.348592803452007} diameter={3.0} />
<hole pcbX={-39.01349290487184} pcbY={31.808592803452} diameter={4.1} />
<hole pcbX={-33.93349290487183} pcbY={31.808592803452} diameter={1.9} />
<hole pcbX={-44.09349290487185} pcbY={31.808592803452} diameter={1.9} />
<hole pcbX={-36.47349290487185} pcbY={36.888592803452} diameter={3.0} />
<hole pcbX={-42.82349290487184} pcbY={34.348592803452} diameter={3.0} />
<hole pcbX={-9.013492904871839} pcbY={-24.191407196548} diameter={4.1} />
<hole pcbX={-3.9334929048718266} pcbY={-24.191407196548} diameter={1.9} />
<hole pcbX={-14.093492904871852} pcbY={-24.191407196548} diameter={1.9} />
<hole pcbX={-6.473492904871847} pcbY={-19.111407196548} diameter={3.0} />
<hole pcbX={-12.823492904871841} pcbY={-21.651407196547993} diameter={3.0} />
<hole pcbX={-31.01349290487184} pcbY={-26.941407196548} diameter={4.1} />
<hole pcbX={-26.106589707323366} pcbY={-25.626606447427193} diameter={1.9} />
<hole pcbX={-35.92039610242031} pcbY={-28.256207945668805} diameter={1.9} />
<hole pcbX={-29.87484205521841} pcbY={-21.37710362443913} diameter={3.0} />
<hole pcbX={-35.35107067759361} pcbY={-25.474056159614364} diameter={3.0} />
<hole pcbX={-54.226224604871845} pcbY={-30.964383896548} diameter={4.1} />
<hole pcbX={-51.68622460487184} pcbY={-35.36379294777295} diameter={1.9} />
<hole pcbX={-56.76622460487185} pcbY={-26.56497484532305} diameter={1.9} />
<hole pcbX={-48.5568155536469} pcbY={-30.62408842216047} diameter={3.0} />
<hole pcbX={-53.93152007925937} pcbY={-26.39482710812929} diameter={3.0} />
<hole pcbX={-68.28849290487184} pcbY={-8.691407196547999} diameter={0.9} />
<hole pcbX={-68.28849290487184} pcbY={-5.691407196547999} diameter={0.9} />
<hole pcbX={-58.71749290487185} pcbY={37.883592803452004} diameter={0.75} />
<hole pcbX={-58.71749290487185} pcbY={35.133592803452004} diameter={0.75} />
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
