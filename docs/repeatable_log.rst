.. _repeatable_log:

=========================
Repeatable pydov sessions
=========================

Pydov can be used to integrate DOV data in your own scripts and analysis. By 
default it will execute a new search operation on every run, making it easy to
rerun your analysis at a later time using the latest data that might not have been
available before. This means your script and analysis will be reproducible.

For some projects or use-cases one might want to go a step further and want
full repeatability: when rerunning the script or analysis exactly the same 
results should be returned. Pydov supports this too, by allowing users to
save (record) a pydov session into an archive and replaying it afterwards.

Recording a pydov session
*************************

To record a pydov session, you can add the following to the top of your script.
It will add an instance of the RepeatableLogRecorder to the pydov hooks, which 
takes a single argument with the directory where the archive will be saved.

   ::

        import pydov
        from pydov.util.hooks import RepeatableLogRecorder

        pydov.hooks.append(
            RepeatableLogRecorder('.')
        )

When running your script, pydov will now create a new zip archive in the 
provided directory and save the entire session inside, including all metadata 
and search query responses, XML data and even pydov itself.

After the script is finished, it will print the location of the archive 
containing the saved session.


Replaying a saved pydov session
*******************************

To replay a recorded session, you can add the following to the top of your 
script. It will prepend the saved session to your Python path, which makes sure
the next import(s) of pydov will import from the recorded archive. Next it
installs the RepeatableLogReplayer hook, which takes a single argument with the
location of the archive.

    ::

        import sys
        sys.path.insert(0, './pydov-archive-20221006T150643-997a6d.zip')

        import pydov
        from pydov.util.hooks import RepeatableLogReplayer

        pydov.hooks.append(
            RepeatableLogReplayer('./pydov-archive-20221006T150643-997a6d.zip')
        )