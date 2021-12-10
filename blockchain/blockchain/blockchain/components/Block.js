import { Card, FormGroup, FormLabel, TextField, Typography } from "@mui/material";

const styles = {
    card: {
        maxWidth: '20rem',
        padding: '1rem',
        backgroundColor: 'rgba(150,150,255,0.2)',
        margin: '1rem'
    },
    formGroup: {
        paddingTop: '0.5rem',
        paddingBottom: '0.5rem',
    },
    text: {
        textWrap: 'wrap',
        overflowWrap: 'break-word',
        wordBreak:'break-all'
    }
}

export default function Block({ index, prevHash, data, hash, blockChange }) {
    return (
        <Card sx={styles.card}>
            <form>
                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Prev Hash</FormLabel>
                    <Typography sx={styles.text}>{prevHash}</Typography>
                </FormGroup>

                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Data</FormLabel>
                    <TextField onChange={e => blockChange(index, e.target.value)} value={data} />
                </FormGroup>

                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Block Hash</FormLabel>
                    <Typography sx={styles.text}>{hash}</Typography>
                </FormGroup>
            </form>
        </Card>
    )
}





// class Block {
//     constructor(index, prevHash, data, hash) {
//         this.index = index;
//         this.prevHas
//         this.data = data;
//         this.timestamp = timestamp;
//         this.data = data;
//         this.previousHash = previousHash;
//         this.hash = this.calculateHash();
//     }

//     createHash(value) {
//         return createHash('sha256').update(value).digest('hex');
//     }

//     calculateHash() {
//         return this.createHash(this.index + this.previousHash + this.timestamp + JSON.stringify(this.data)).toString();
//     }

//     render() {
//         return (
//             <Card sx={styles.card}>
//                 <form>
//                     <FormGroup sx={styles.formGroup}>
//                         <FormLabel>Prev Hash</FormLabel>
//                         <Typography sx={styles.text}>{this.previousHash}</Typography>
//                     </FormGroup>

//                     <FormGroup sx={styles.formGroup}>
//                         <FormLabel>Data</FormLabel>
//                         <TextField onChange={e => setBlockChain(blockChain.slice(0, index).concat([]))} value={data} />
//                     </FormGroup>

//                     <FormGroup sx={styles.formGroup}>
//                         <FormLabel>Block Hash</FormLabel>
//                         <Typography sx={styles.text}>{hashData()}</Typography>
//                     </FormGroup>
//                 </form>
//             </Card>
//         )
//     }
// }