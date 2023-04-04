import {useEffect, useState} from "react";
import TableComponent, {Supply} from "../tableComponent/TableComponent";
import SupplyService from "../../services/supplyService";


const BodyComponent = () => {
    const [supplies, setSupplies] = useState<Array<Supply>>([]);

    useEffect(() => {
        SupplyService.getSupplies().then((response) => {
            setSupplies(response.data);
        })
    }, [])

    return (
        <div className={"body-component"}>
            <TableComponent supplies={supplies}/>

        </div>
    )
}

export default BodyComponent;