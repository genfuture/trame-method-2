# myapp/management/commands/start_trame.py
from django.core.management.base import BaseCommand
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera  # noqa
import vtkmodules.vtkRenderingOpenGL2  # noqa

class Command(BaseCommand):
    help = 'Start the Trame server'

    def handle(self, *args, **kwargs):
        # VTK pipeline setup
        renderer = vtkRenderer()
        renderWindow = vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        # Set the interactor style
        interactorStyle = vtkInteractorStyleTrackballCamera()
        renderWindowInteractor.SetInteractorStyle(interactorStyle)

        cone_source = vtkConeSource()
        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(cone_source.GetOutputPort())
        actor = vtkActor()
        actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()

        # Trame server setup
        server = get_server(client_type="vue2")
        ctrl = server.controller

        with SinglePageLayout(server) as layout:
            layout.title.set_text("Hello trame")
            with layout.content:
                with vuetify.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    view = vtk.VtkLocalView(renderWindow)

        server.start()
