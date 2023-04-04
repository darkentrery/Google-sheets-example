import {FC} from "react";


interface TableProps {
    count: number;
}

const CountComponent: FC<TableProps> = ({count}) => {
    return (
        <div className={"count-component"}>
            <div className={"head"}>Total</div>
            <div className={"row"}>{count}</div>
        </div>
    )
}

export default CountComponent;