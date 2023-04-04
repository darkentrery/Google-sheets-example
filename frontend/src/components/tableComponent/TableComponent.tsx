import {FC} from "react";

export interface Supply {
    number: number;
    order: number;
    cost: number;
    cost_rub: number;
    date: string;
}

interface TableProps {
    supplies: Supply[] | [];
}

const TableComponent: FC<TableProps> = ({supplies}) => {

    return (
        <div className={"table-component"}>
            <div className={"table-head"}>
                <div className={"cell cell-1"}>№</div>
                <div className={"cell cell-2"}>Заказ №</div>
                <div className={"cell cell-3"}>Стоимость, $</div>
                <div className={"cell cell-4"}>Стоимость, P</div>
                <div className={"cell cell-5"}>Срок поставки</div>
            </div>
            <div className={"table-body"}>
                {supplies.map((supply, i) => (
                    <div className={"row"} key={i}>
                        <div className={"cell cell-1"}>{supply.number}</div>
                        <div className={"cell cell-2"}>{supply.order}</div>
                        <div className={"cell cell-3"}>{supply.cost}</div>
                        <div className={"cell cell-4"}>{supply.cost_rub}</div>
                        <div className={"cell cell-5"}>
                            {new Date(supply.date).toLocaleDateString('en-GB', {
                                day: 'numeric',
                                month: 'numeric',
                                year: 'numeric'
                            }).split("/").join(".")}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default TableComponent;