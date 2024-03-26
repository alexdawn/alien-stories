import { type } from "../../util/io.js";


const output = [
    'NO. 62.584-EM.ICC2',
    '',
    'CONTRACT'
];

const players = {
    miller: {name: 'Chunk Miller', role: 'security consultant', pay: '400'},
    champlain: {name: 'Oliva De Champlain', role: 'captain', pay: '850'},
    morgan: {name: 'Llyod Morgan', role: 'medical officer', pay: '700'},
    callahan: {name: 'Victor Callhan', role: 'scientist', pay: '1500', forfeit: 'including a bonus of 200 for having sub-contract his colonial rights to religion'}
}

const fullOutput = (name, role, pay, forfeit) => `
This binding contract is signed between ${name}
employed as a ${role} aboard the UNCSS Solovetsky island
and the United Nations Interstellar Settlement Corps, for a minimum
duration of either: four years; or one day after all the Far Spinward
colonies have been formally assessed (whichever is the sooner), at
the rate of ${pay} Weyland-Yutani dollars per expedition week, ${forfeit ?? ''}
(one-quarter pay during periods of hypersleep).

---------------------------------------------------------
The mission parameters-and your responsibilities under this
contract-are as follows:
1. Establish contact with the Far Spinward Colonies and provide
    immediate humanitarian support as necessary.
2. Survey the sector and establish new UN-administered colonies.
3. Recover existing Colonial records for each colony, stored in
    local Long Data Discs.
4. Negotiate terms under which surviving colonies should return to
    UNISC oversight.
5. Assess the future technological, industrial and financial potential.
6. Adhere to all Interstellar Commerce Commission protocols and
    regulations and collaborate in the spirit of the greater good.

-----------------------------------------------------------------

The Great Mother Mission consists of the Colony Vessel UNCSS
İyánlá, the four Science Exploration Vessels, UNCSS Umsindisi,
Solovetsky Island, Chimata-no-kami and Typhoon, and the three
support vessels of Throop Rescue & Recovery. Crew is from the
Three World Empire, United Americas, Union of Progressive Peoples
and independent contractors, with sponsorship by Weyland-Yutani,
Hyperdyne Corporation, Omni-Tech Resources and the Kelland
Mining Company. The mission comes under the auspices of the
United Nations Interstellar Settlement Corps, under the command of
UN Governor Kholwa Abantu.

------------------------------------------------------------------

Additional bonus salary may be earned for finds, discoveries or
resource rights once any claim has been registered, logged, passed
all Interstellar Commerce Commission regulatory checks (including
obligatory quarantine requirements, where necessary) and its value
formally assessed.

------------------------------------------------------------------

All wages will be forfeit if you fail to meet your responsibilities and
/ or your conduct fails to reach the minimum standards of behavior
and professionalism, as noted in the Articles of Employment, pages
17-51.

Welcome aboard the
Great Mother Mission!
ICC
`;

async function contract(name) {
    if (name in players) {
        const player = players[name];
        await type(fullOutput(player.name, player.role, player.pay, player.forfeit ?? ''));
    } else {
        await type(`name ${name} not recognised`);
    }
    
}

export { output };

export default contract;
