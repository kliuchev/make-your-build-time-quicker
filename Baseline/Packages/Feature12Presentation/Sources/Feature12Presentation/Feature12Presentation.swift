import Feature12Domain
import Feature12Data

public enum Feature12PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature12DomainModel = Feature12DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
