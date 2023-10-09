import { Stack } from "@mui/material";
import { Box, styled } from "@mui/system";
import { Breadcrumb, SimpleCard } from "app/components";
import SimpleForm from "./SimpleForm";
import axios from "axios";
import { BASE_BACKEND, BASE_FLOW } from "app/utils/constant";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchOutlet } from "app/utils/fetchData";

const Container = styled("div")(({ theme }) => ({
    margin: "30px",
    [theme.breakpoints.down("sm")]: { margin: "16px" },
    "& .breadcrumb": {
        marginBottom: "30px",
        [theme.breakpoints.down("sm")]: { marginBottom: "16px" },
    },
}));


const AppFlowCreate = () => {
    const navigate = useNavigate()
    const [outletContent, setOutletContent] = useState([])

    const handleSubmit = (event, state) => {
        axios.post(BASE_BACKEND+BASE_FLOW,state)
            .then((response) => {navigate('/flows')})
    }

    useEffect(() => {
        fetchOutlet(setOutletContent)
    },[])

    return (
        <Container>
            <Box className="breadcrumb">
                <Breadcrumb routeSegments={[{ name: "flows", path: "/flows" }, { name: "Create" }]} />
            </Box>

            <Stack spacing={3}>
                <SimpleCard title="New Flow">
                    <SimpleForm sendData={handleSubmit} outlets={outletContent} />
                </SimpleCard>
            </Stack>
        </Container>
    );
};

export default AppFlowCreate;
