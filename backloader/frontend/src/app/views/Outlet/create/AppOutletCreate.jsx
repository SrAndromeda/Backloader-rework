import { Stack } from "@mui/material";
import { Box, styled } from "@mui/system";
import { Breadcrumb, SimpleCard } from "app/components";
import SimpleForm from "./SimpleForm";
import axios from "axios";
import { BASE_BACKEND, BASE_OUTLET } from "app/utils/constant";
import { useNavigate } from "react-router-dom";

const Container = styled("div")(({ theme }) => ({
    margin: "30px",
    [theme.breakpoints.down("sm")]: { margin: "16px" },
    "& .breadcrumb": {
        marginBottom: "30px",
        [theme.breakpoints.down("sm")]: { marginBottom: "16px" },
    },
}));


const AppOutletCreate = () => {
    const navigate = useNavigate()

    const handleSubmit = (event, state) => {
        axios.post(BASE_BACKEND+BASE_OUTLET,state)
            .then((response) => {navigate('/outlets')})
    }

    return (
        <Container>
            <Box className="breadcrumb">
                <Breadcrumb routeSegments={[{ name: "Outlets", path: "/outlets" }, { name: "Create" }]} />
            </Box>

            <Stack spacing={3}>
                <SimpleCard title="New Outlet">
                    <SimpleForm sendData={handleSubmit} />
                </SimpleCard>
            </Stack>
        </Container>
    );
};

export default AppOutletCreate;
