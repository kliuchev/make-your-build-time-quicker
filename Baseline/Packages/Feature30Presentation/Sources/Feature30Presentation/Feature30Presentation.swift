import Feature30Domain
import Feature30Data

public enum Feature30PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature30DomainModel = Feature30DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
