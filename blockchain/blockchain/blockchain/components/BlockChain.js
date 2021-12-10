import Block from './Block';
import { createHash } from 'crypto';
import { useEffect, useState } from 'react';
import { Button } from '@mui/material';

const hashData = (value) => {
    return createHash('sha256').update(value).digest('hex');
}

export default function BlockChain() {
    const [ values, setValues ] = useState([ "Hello world" ]);
    const [ blockChainData, setBlockChainData ] = useState([]);
    const initialHash = '0000';

    const blockChange = (index, data) => {
        const newVals = values;
        newVals[index] = data;
        setValues(newVals);
        calcBlockChainData();
    }

    const calcBlockChainData = () => {
        const data = [];
        let prevHash = initialHash;
        for (let i=0; i<values.length; i++) {
            let hash = hashData(`${prevHash}.${values[i]}`);
            data.push({
                index: i,
                prevHash,
                data: values[i],
                hash 
            });
            prevHash = hash;
        }
        setBlockChainData(data);
    }

    const addBlock = () => {
        const vals = values;
        vals.push([ "New block!" ]);
        setValues(vals);
        calcBlockChainData();
    }

    useEffect(() => { calcBlockChainData() }, [])

    return (
        <div>
            {blockChainData.map(b => (
                <Block index={b.index}
                    prevHash={b.prevHash}
                    data={b.data}
                    hash={b.hash}
                    blockChange={blockChange} 
                />
            ))}
            <Button onClick={addBlock}>Add block</Button>
        </div>
    )
}