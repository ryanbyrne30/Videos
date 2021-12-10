import { Card, FormGroup, FormLabel, TextField, Typography } from "@mui/material";
import { createHash } from 'crypto';
import { useState } from "react";

const randColorComponent = () => {
    return Math.floor(Math.random()*255);
}

const randColor = () =>  {
    const r = randColorComponent();
    const g = randColorComponent();
    const b = randColorComponent();
    return `rgba(${r},${g},${b}, 0.2)`;
}

const styles = {
    card: {
        maxWidth: '20rem',
        padding: '1rem',
        backgroundColor: randColor()
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

export default function Block({ prevHash, data, setData }) {
    const [ data, setData ] = useState("");

    const hashData = () => {
        return createHash('sha256').update(data).digest('hex');
    }

    return (
        <Card sx={styles.card}>
            <form>
                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Prev Hash</FormLabel>
                    <Typography sx={styles.text}>{prevHash}</Typography>
                </FormGroup>

                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Data</FormLabel>
                    <TextField onChange={e => setData(e.target.value)} value={data} />
                </FormGroup>

                <FormGroup sx={styles.formGroup}>
                    <FormLabel>Block Hash</FormLabel>
                    <Typography sx={styles.text}>{hashData()}</Typography>
                </FormGroup>
            </form>
        </Card>
    )
}