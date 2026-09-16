import Feature16Domain
import Feature16Data

public enum Feature16PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature16DomainModel = Feature16DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
