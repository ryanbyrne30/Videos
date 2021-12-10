import Block from './Block';
import { createHash } from 'crypto';

const hashData = (value) => {
    return createHash('sha256').update(value).digest('hex');
}

export default function BlockChain() {
    const [ values, setValues ] = useState([]);
    const initialHash = "000000000";

    const renderBlocks = () => {
        const blocks = [];

        for (let i=0; i<values.length; i++) {
            let prevHash = initialHash;
            let hash = hashData(`${prevHash}.${values[i]}`);
            blocks.push({
                prevHash,
                value: values[i],
                hash
            });
        }
    }

    return (
        <div>

        </div>
    )
}